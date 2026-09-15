"""BoardState derivation — turn a project directory into renderable state.

Everything here is read-only and defensive: a malformed JSON file, a missing
artifact, or a half-written checkpoint must degrade the board, never crash it
(design principle: "never block, never break").
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from lib.events import read_events
from lib.paths import PROJECTS_DIR, REPO_ROOT  # single source of truth (env-overridable)

MEDIA_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
MEDIA_VIDEO_EXT = {".mp4", ".webm", ".mov"}
MEDIA_AUDIO_EXT = {".mp3", ".wav", ".m4a", ".ogg"}

# Directories inside a project we never scan for media (build noise).
SCAN_EXCLUDE = {"node_modules", ".git", "__pycache__", "history", ".cache"}

# Stages every pipeline shares (fallback rail when the manifest is unknown).
FALLBACK_STAGES = [
    "research", "proposal", "idea", "script", "scene_plan",
    "assets", "edit", "compose", "publish",
]

# How long (seconds) without filesystem activity before a board reads "idle".
LIVE_WINDOW_SECONDS = 5 * 60

# An in_progress stage with no filesystem activity for this long is flagged
# as possibly stalled (F-05: a wedged agent must be visible, not silent —
# heartbeat checkpoints and tool events both reset the clock).
STALL_WINDOW_SECONDS = 10 * 60


def _read_json(path: Path) -> Optional[dict]:
    """Read a JSON file, returning None on any failure."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except (OSError, json.JSONDecodeError, UnicodeError):
        return None


def _read_contained_project_json(project_dir: Path, path: Path) -> Optional[dict]:
    """Read one regular JSON file only when its resolved target stays local."""
    try:
        root = Path(project_dir).resolve()
        resolved = Path(path).resolve(strict=True)
        resolved.relative_to(root)
    except (ValueError, OSError):
        return None
    if not resolved.is_file():
        return None
    return _read_json(resolved)


def _rel(project_dir: Path, path: Path) -> str:
    """Project-relative POSIX path for media URLs."""
    try:
        return path.resolve().relative_to(Path(project_dir).resolve()).as_posix()
    except (ValueError, OSError):
        return path.name


# ---------------------------------------------------------------------------
# Pipeline / stages
# ---------------------------------------------------------------------------

@lru_cache(maxsize=32)
def _load_pipeline_meta(pipeline_type: Optional[str]) -> dict[str, Any]:
    """Stage order + gate flags from the manifest; graceful fallback."""
    if pipeline_type and pipeline_type != "unknown":
        try:
            from lib.pipeline_loader import load_pipeline
            manifest = load_pipeline(pipeline_type)
            stages = [
                {
                    "name": s["name"],
                    "gated": bool(s.get("human_approval_default", False)),
                    "produces": [
                        str(name) for name in (s.get("produces") or [])
                        if isinstance(name, str) and name
                    ],
                }
                for s in manifest.get("stages", [])
                if isinstance(s, dict) and s.get("name")
            ]
            if stages:
                return {
                    "pipeline_type": pipeline_type,
                    "stages": stages,
                    "known": True,
                }
        except Exception:
            pass
    return {
        "pipeline_type": pipeline_type or "unknown",
        "stages": [{"name": s, "gated": False, "produces": []} for s in FALLBACK_STAGES],
        "known": False,
    }


def _resolve_artifact(project_dir: Path, value: Any) -> Optional[dict]:
    """Checkpoint artifacts may be inline dicts or path strings — resolve both.

    Path references are only followed INSIDE the project directory: a
    checkpoint must not be able to pull arbitrary JSON from elsewhere on
    disk onto the board (F-04).
    """
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value:
        p = Path(value)
        if not p.is_absolute():
            p = project_dir / value
        return _read_contained_project_json(project_dir, p)
    return None


def _collect_checkpoints(project_dir: Path) -> dict[str, dict]:
    """Current checkpoint per stage, validated under its physical project root.

    Loader metadata must never be inserted into the checkpoint object.  Gate
    verification validates the full envelope with ``additionalProperties:
    false``; mutating the object here and later stripping private-looking keys
    would make a malicious on-disk ``_...`` field indistinguishable from
    trusted BoardState metadata.
    """
    out: dict[str, dict] = {}
    for path in sorted(project_dir.glob("checkpoint_*.json")):
        stage = path.stem[len("checkpoint_"):]
        data = _read_contained_project_json(project_dir, path)
        if data is None:
            continue
        try:
            if data.get("project_id") != project_dir.name or data.get("stage") != stage:
                raise ValueError(
                    "checkpoint filename/project identity does not match its envelope"
                )
            from lib.checkpoint import validate_checkpoint

            # Lifecycle truth must match runtime resume exactly.  Validate the
            # raw envelope; do not make a path-backed legacy artifact look valid
            # merely because the board can materialize it for display.
            validate_checkpoint(data, pipeline_dir=project_dir.parent)
            out[stage] = data
        except Exception as exc:
            # Preserve the raw envelope for diagnostics, but make invalidity a
            # trusted BoardState annotation and never honor lifecycle/approval
            # fields from the rejected checkpoint.
            rejected = dict(data)
            rejected["_checkpoint_invalid"] = True
            rejected["_checkpoint_validation_error"] = str(exc)
            out[stage] = rejected
    return out


def _collect_history(project_dir: Path) -> dict[str, list[dict]]:
    """Archived lifecycle snapshots per stage (oldest first).

    History drives display replay only; it is never authority. Keep only a
    schema-safe status/timestamp pair so malformed NaN/Infinity or forged raw
    lifecycle fields cannot break JSON serialization or overwrite an invalid
    current state during replay.
    """
    history_dir = project_dir / "history"
    out: dict[str, list[dict]] = {}
    if not history_dir.is_dir():
        return out
    for path in sorted(history_dir.glob("checkpoint_*.json")):
        m = re.match(r"checkpoint_(.+?)_\d", path.stem)
        stage = m.group(1) if m else path.stem[len("checkpoint_"):]
        data = _read_contained_project_json(project_dir, path)
        if data is not None:
            status = data.get("status")
            timestamp = data.get("timestamp")
            valid = status in {
                "pending",
                "in_progress",
                "awaiting_human",
                "completed",
                "failed",
            }
            if valid:
                try:
                    from lib.checkpoint import _validate_rfc3339_timestamp

                    _validate_rfc3339_timestamp(timestamp, "history timestamp")
                except Exception:
                    valid = False
            out.setdefault(stage, []).append({
                "status": status if valid else "invalid",
                "timestamp": timestamp if valid else None,
            })
    return out


def _checkpoint_mtime(project_dir: Path, stage: str) -> float:
    """Return checkpoint freshness without contaminating its JSON envelope."""
    try:
        root = Path(project_dir).resolve()
        path = (root / f"checkpoint_{stage}.json").resolve(strict=True)
        path.relative_to(root)
        return path.stat().st_mtime if path.is_file() else 0.0
    except (ValueError, OSError):
        return 0.0


def _resolve_checkpoint_artifacts(
    project_dir: Optional[Path], checkpoint: dict[str, Any]
) -> Optional[dict[str, dict]]:
    """Resolve every artifact in one checkpoint without leaving its project root.

    The board accepts both inline artifact objects and legacy/project-relative
    JSON paths.  Gate evidence must never mix a raw checkpoint value with an
    artifact discovered elsewhere on the board, so resolution is performed
    against the checkpoint's own artifact map and fails closed as a unit.
    """
    raw_artifacts = checkpoint.get("artifacts")
    if not isinstance(raw_artifacts, dict):
        return None

    resolved: dict[str, dict] = {}
    for name, value in raw_artifacts.items():
        if not isinstance(name, str) or not name:
            return None
        if isinstance(value, dict):
            artifact = value
        elif project_dir is not None:
            artifact = _resolve_artifact(project_dir, value)
        else:
            artifact = None
        if not isinstance(artifact, dict):
            return None
        resolved[name] = artifact
    return resolved


def _resolved_checkpoint(
    project_dir: Optional[Path], checkpoint: Any
) -> Optional[dict[str, Any]]:
    """Materialize one schema-facing checkpoint without BoardState metadata."""
    if not isinstance(checkpoint, dict):
        return None
    resolved_artifacts = _resolve_checkpoint_artifacts(project_dir, checkpoint)
    if resolved_artifacts is None:
        return None
    # Copy every raw key. Unknown fields (including names beginning with an
    # underscore) must reach the shared checkpoint schema and fail closed.
    clean_checkpoint = dict(checkpoint)
    clean_checkpoint["artifacts"] = resolved_artifacts
    return clean_checkpoint


def _resolved_predecessor_checkpoint(
    project_dir: Optional[Path],
    checkpoints: dict[str, dict],
) -> Optional[dict[str, Any]]:
    """Resolve the exact script checkpoint within the current project root.

    This helper only materializes the candidate bundle.  The shared gate verifier
    remains the single authority for checkpoint identity, status, approval,
    schema, and provenance validation.
    """
    script_checkpoint = checkpoints.get("script")
    resolved = _resolved_checkpoint(project_dir, script_checkpoint)
    if not isinstance(resolved, dict):
        return None
    artifacts = resolved.get("artifacts")
    if not isinstance(artifacts, dict) or not isinstance(artifacts.get("script"), dict):
        return None
    return resolved


def _has_valid_zero_entity_auto_pass(
    project_dir: Optional[Path],
    checkpoint: Any,
    checkpoints: dict[str, dict],
) -> bool:
    """Use the shared gate verifier with one project-root-resolved bundle."""
    if not isinstance(checkpoint, dict) or project_dir is None:
        return False
    try:
        from lib.identity import resolve_project_dir

        requested_project_dir = Path(project_dir)
        physical_project_id = requested_project_dir.name
        safe_project_dir = resolve_project_dir(
            requested_project_dir.parent, physical_project_id
        )
        if checkpoint.get("project_id") != physical_project_id:
            return False

        resolved_checkpoint = _resolved_checkpoint(safe_project_dir, checkpoint)
        if resolved_checkpoint is None:
            return False
        resolved_artifacts = resolved_checkpoint["artifacts"]
        predecessor_checkpoint = _resolved_predecessor_checkpoint(
            safe_project_dir, checkpoints
        )
        if predecessor_checkpoint is None:
            return False
        if predecessor_checkpoint.get("project_id") != physical_project_id:
            return False

        from lib.checkpoint import verify_gate_resolution

        is_valid, _ = verify_gate_resolution(
            resolved_checkpoint,
            resolved_artifacts,
            predecessor_checkpoint=predecessor_checkpoint,
            pipeline_dir=safe_project_dir.parent,
        )
        return bool(is_valid)
    except Exception:
        # BoardState is observational.  Truncated, malformed, or path-escaped
        # evidence degrades to an unverified badge and must never break the board.
        return False


def _build_stage_rail(
    pipeline_meta: dict,
    checkpoints: dict[str, dict],
    history: dict[str, list[dict]],
    project_dir: Optional[Path] = None,
) -> list[dict]:
    """One entry per manifest stage with derived status + gate audit."""
    rail = []
    manifest_stage_names = {s["name"] for s in pipeline_meta["stages"]}
    for stage_def in pipeline_meta["stages"]:
        name = stage_def["name"]
        raw_checkpoint = checkpoints.get(name)
        cp = raw_checkpoint if isinstance(raw_checkpoint, dict) else None
        versions = history.get(name, [])
        checkpoint_invalid = bool(cp and cp.get("_checkpoint_invalid"))
        status = "invalid" if checkpoint_invalid else (cp.get("status") if cp else "pending")
        metadata = (
            cp.get("metadata")
            if isinstance(cp, dict) and not checkpoint_invalid
            else None
        )
        entry: dict[str, Any] = {
            "name": name,
            "gated": stage_def["gated"],
            "produces": list(stage_def.get("produces") or []),
            "status": status or "pending",
            "timestamp": cp.get("timestamp") if cp and not checkpoint_invalid else None,
            "review": cp.get("review") if cp and not checkpoint_invalid else None,
            "cost_snapshot": cp.get("cost_snapshot") if cp and not checkpoint_invalid else None,
            "error": (
                cp.get("_checkpoint_validation_error")
                if checkpoint_invalid
                else (cp.get("error") if cp else None)
            ),
            "human_approved": cp.get("human_approved") if cp and not checkpoint_invalid else None,
            "gate_resolution": cp.get("gate_resolution") if cp and not checkpoint_invalid else None,
            "checkpoint_invalid": checkpoint_invalid,
            "partial_progress": metadata.get("partial_progress") if isinstance(metadata, dict) else None,
            "versions": len(versions) + (1 if cp else 0),
            # Chronological status trail (history + current) — powers replay.
            "history_entries": (
                [{"status": v.get("status"), "timestamp": v.get("timestamp")} for v in versions]
                + ([{
                    "status": "invalid" if checkpoint_invalid else cp.get("status"),
                    "timestamp": None if checkpoint_invalid else cp.get("timestamp"),
                }] if cp else [])
            ),
        }
        # CLP gate truth comes exclusively from the shared verifier, supplied
        # with artifacts and its predecessor resolved within this project root.
        is_verified_auto_passed = not checkpoint_invalid and name == "clp" and _has_valid_zero_entity_auto_pass(
            project_dir, cp, checkpoints
        )

        if is_verified_auto_passed:
            entry["auto_passed"] = True
            entry["gate_skipped"] = False
        else:
            entry["auto_passed"] = False
            if (
                not checkpoint_invalid
                and
                cp is not None
                and cp.get("status") == "completed"
                and cp.get("human_approved") is not True
                and (stage_def["gated"] or name == "clp")
            ):
                # Historical ``awaiting_human`` is evidence that a gate was
                # reached, never evidence that a human approved it.  An
                # unapproved completed CLP checkpoint is also a skip unless the
                # shared typed zero-entity verifier accepted it above.
                entry["gate_skipped"] = True
            else:
                entry["gate_skipped"] = False
        rail.append(entry)

    # Checkpoints for stages the manifest doesn't declare (legacy runs,
    # pipeline mismatch) still deserve a slot — at their canonical position
    # in the pipeline, not dangling after publish ("idea" belongs up front).
    canon = {name: i for i, name in enumerate(FALLBACK_STAGES)}
    for name, cp in checkpoints.items():
        if name in manifest_stage_names:
            continue
        checkpoint_invalid = bool(cp.get("_checkpoint_invalid"))
        entry = {
            "name": name,
            "gated": False,
            "produces": [
                str(artifact_name)
                for artifact_name in (cp.get("artifacts") or {})
                if isinstance(artifact_name, str) and artifact_name
            ],
            "status": "invalid" if checkpoint_invalid else (cp.get("status") or "unknown"),
            "timestamp": None if checkpoint_invalid else cp.get("timestamp"),
            "review": None if checkpoint_invalid else cp.get("review"),
            "cost_snapshot": None if checkpoint_invalid else cp.get("cost_snapshot"),
            "error": cp.get("_checkpoint_validation_error") if checkpoint_invalid else cp.get("error"),
            "human_approved": None if checkpoint_invalid else cp.get("human_approved"),
            "checkpoint_invalid": checkpoint_invalid,
            "partial_progress": None,
            "versions": 1 + len(history.get(name, [])),
            "undeclared": True,
        }
        pos = canon.get(name)
        if pos is None:
            rail.append(entry)  # truly unknown name — end of rail
            continue
        insert_at = len(rail)
        for i, existing in enumerate(rail):
            existing_pos = canon.get(existing["name"])
            if existing_pos is not None and existing_pos > pos:
                insert_at = i
                break
        rail.insert(insert_at, entry)
    return rail


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------

ARTIFACT_FILES = {
    "research_brief": "research_brief.json",
    "brief": "brief.json",
    "proposal_packet": "proposal_packet.json",
    "script": "script.json",
    "scene_plan": "scene_plan.json",
    "asset_manifest": "asset_manifest.json",
    "edit_decisions": "edit_decisions.json",
    "render_report": "render_report.json",
    "final_review": "final_review.json",
    "publish_log": "publish_log.json",
    "decision_log": "decision_log.json",
    "character_design": "character_design.json",
    "clp_manifest": "clp_manifest.json",
    "clp_candidates": "clp_candidates.json",
    "clp_shot_bindings": "clp_shot_bindings.json",
}

CLP_ARTIFACT_OWNERS = {
    "clp_manifest": "clp",
    "clp_candidates": "clp",
    "clp_shot_bindings": "scene_plan",
}


def _batch_v2_asset_manifest_authority(
    project_dir: Path, checkpoint: Any
) -> tuple[bool, Optional[dict], Optional[str]]:
    """Classify only an explicit Batch V2 assets publication claim."""

    if not isinstance(checkpoint, dict) or checkpoint.get("_checkpoint_invalid"):
        return False, None, None
    metadata = (checkpoint.get("metadata") or {}).get("batch_v2_publication")
    if not isinstance(metadata, dict) or metadata.get("kind") != (
        "batch_v2_assets_publication"
    ):
        return False, None, None
    try:
        from lib.batch_executor.publication import (
            inspect_v2_asset_manifest_claim,
        )

        return inspect_v2_asset_manifest_claim(project_dir, checkpoint)
    except Exception:
        return True, None, "batch_v2_publication_validator_unavailable"


def _collect_artifacts(
    project_dir: Path, checkpoints: dict[str, dict]
) -> tuple[dict[str, dict], list[dict[str, str]]]:
    """Collect display artifacts without creating a second CLP truth source.

    Ordinary standalone artifacts retain their historical precedence.  CLP
    artifacts are different: runtime execution is authorized by validated
    owning checkpoints, so a standalone file is only a cache and can never
    override (or substitute for) that checkpoint authority.
    """
    artifacts: dict[str, dict] = {}
    diagnostics: list[dict[str, str]] = []
    art_dir = project_dir / "artifacts"
    for name, filename in ARTIFACT_FILES.items():
        if name in CLP_ARTIFACT_OWNERS:
            continue
        data = _read_contained_project_json(project_dir, art_dir / filename)
        if data is not None:
            artifacts[name] = data
    # decision_log historically also lives at project root
    if "decision_log" not in artifacts:
        data = _read_contained_project_json(
            project_dir, project_dir / "decision_log.json"
        )
        if data is not None:
            artifacts["decision_log"] = data
    # Backfill from checkpoint-embedded artifacts.
    for cp in checkpoints.values():
        if cp.get("_checkpoint_invalid"):
            continue
        for name, value in (cp.get("artifacts") or {}).items():
            if name in CLP_ARTIFACT_OWNERS:
                continue
            if name not in artifacts:
                resolved = _resolve_artifact(project_dir, value)
                if resolved is not None:
                    artifacts[name] = resolved

    from lib.clp_validator import canonical_digest

    for name, owner_stage in CLP_ARTIFACT_OWNERS.items():
        cache = _read_contained_project_json(
            project_dir, art_dir / ARTIFACT_FILES[name]
        )
        checkpoint = checkpoints.get(owner_stage) or {}
        authoritative = None
        if not checkpoint.get("_checkpoint_invalid"):
            authoritative = _resolve_artifact(
                project_dir, (checkpoint.get("artifacts") or {}).get(name)
            )
        if authoritative is None:
            if cache is not None:
                diagnostics.append({
                    "artifact": name,
                    "status": "untrusted_cache_ignored",
                    "reason": f"missing valid checkpoint_{owner_stage}.json authority",
                })
            continue
        artifacts[name] = authoritative
        if cache is not None:
            try:
                cache_matches = canonical_digest(cache) == canonical_digest(authoritative)
            except (TypeError, ValueError):
                diagnostics.append({
                    "artifact": name,
                    "status": "invalid_cache_ignored",
                    "reason": "standalone cache is not canonical JSON",
                })
            else:
                if not cache_matches:
                    diagnostics.append({
                        "artifact": name,
                        "status": "cache_mismatch_ignored",
                        "reason": f"checkpoint_{owner_stage}.json remains authoritative",
                    })

    # Batch V2 makes only its explicitly tagged, officially validated assets
    # checkpoint authoritative.  Do not generalize this precedence rule: old
    # projects and every non-V2 artifact retain the legacy behavior above.
    v2_claimed, v2_asset_manifest, v2_claim_error = _batch_v2_asset_manifest_authority(
        project_dir, checkpoints.get("assets")
    )
    if v2_claimed and v2_asset_manifest is None:
        artifacts.pop("asset_manifest", None)
        diagnostics.append({
            "artifact": "asset_manifest",
            "status": "batch_v2_authority_invalid",
            "reason": v2_claim_error or "batch_v2_publication_binding_invalid",
        })
    elif v2_asset_manifest is not None:
        loose_asset_manifest = _read_contained_project_json(
            project_dir, art_dir / ARTIFACT_FILES["asset_manifest"]
        )
        artifacts["asset_manifest"] = v2_asset_manifest
        if loose_asset_manifest is not None:
            try:
                loose_matches = canonical_digest(loose_asset_manifest) == canonical_digest(
                    v2_asset_manifest
                )
            except (TypeError, ValueError):
                diagnostics.append({
                    "artifact": "asset_manifest",
                    "status": "invalid_cache_ignored",
                    "reason": "standalone cache is not canonical JSON",
                })
            else:
                if not loose_matches:
                    diagnostics.append({
                        "artifact": "asset_manifest",
                        "status": "cache_mismatch_ignored",
                        "reason": "validated Batch V2 checkpoint_assets.json remains authoritative",
                    })
    return artifacts, diagnostics


# ---------------------------------------------------------------------------
# Storyboard join
# ---------------------------------------------------------------------------

def _resolve_asset_path(project_dir: Path, raw_path: str) -> Optional[Path]:
    """Manifest paths appear in several real-world flavors — try them all.

    Observed on disk: project-relative ("assets/images/x.png"),
    repo-relative ("projects/<id>/assets/images/x.png"), and absolute.
    """
    if not raw_path:
        return None
    p = Path(raw_path)
    candidates = []
    if p.is_absolute():
        candidates.append(p)
    else:
        candidates.append(project_dir / raw_path)
        candidates.append(REPO_ROOT / raw_path)
        # repo-relative with the project prefix repeated
        parts = p.parts
        if len(parts) > 2 and parts[0] == "projects":
            candidates.append(project_dir.parent / Path(*parts[1:]))
    for c in candidates:
        try:
            if c.is_file():
                return c
        except OSError:
            continue
    return None


def _asset_entry(project_dir: Path, asset: dict) -> dict:
    """Normalize a manifest asset entry + resolve file existence.

    A file that resolves OUTSIDE the project directory is treated as
    not-servable (exists=False): /media only serves within the project, and
    a bare-filename fallback path would 404 or hit the wrong file.
    """
    raw_path = asset.get("path") or ""
    resolved = _resolve_asset_path(project_dir, raw_path)
    if resolved is not None:
        try:
            resolved.resolve().relative_to(Path(project_dir).resolve())
        except (ValueError, OSError):
            resolved = None
    file_path = resolved if resolved is not None else (project_dir / raw_path)
    exists = resolved is not None
    kind = asset.get("type") or ""
    if not kind and file_path.suffix:
        ext = file_path.suffix.lower()
        if ext in MEDIA_IMAGE_EXT:
            kind = "image"
        elif ext in MEDIA_VIDEO_EXT:
            kind = "video"
        elif ext in MEDIA_AUDIO_EXT:
            kind = "audio"
    # A visual is only *renderable* on the board if the file it points at is
    # actually a raster image or a video. Bespoke/atelier assets (type
    # "animation" pointing at a .tsx composition) exist on disk but can't be
    # thumbnailed — routing them to <img> yields a broken image. The board
    # falls back to a per-scene snapshot or the shot-spec placeholder instead.
    ext = file_path.suffix.lower()
    renderable = exists and ext in (MEDIA_IMAGE_EXT | MEDIA_VIDEO_EXT)
    return {
        "id": asset.get("id"),
        "type": kind,
        "scene_id": asset.get("scene_id"),
        "path": _rel(project_dir, file_path) if exists else raw_path,
        "exists": exists,
        "renderable": renderable,
        "prompt": asset.get("prompt"),
        "model": asset.get("model"),
        "source_tool": asset.get("source_tool"),
        "provider": asset.get("provider"),
        "cost_usd": asset.get("cost_usd"),
        "quality_score": asset.get("quality_score"),
        "duration_seconds": asset.get("duration_seconds"),
        "resolution": asset.get("resolution"),
    }


def _find_scene_snapshot(project_dir: Path, scene_id: str) -> Optional[dict]:
    """A per-scene review still, if the run wrote one.

    Atelier/animation scenes have no thumbnailable asset file, so the
    assets-stage snapshot (`snapshots/<scene_id>.png`) is what the filmstrip
    shows. Accept exact `<scene_id>.<ext>` and `<scene_id>_*.<ext>` forms.
    """
    snap_dir = project_dir / "snapshots"
    if not scene_id or not snap_dir.is_dir():
        return None
    try:
        for f in sorted(snap_dir.iterdir()):
            if not f.is_file() or f.suffix.lower() not in MEDIA_IMAGE_EXT:
                continue
            stem = f.stem
            if stem == scene_id or stem.startswith(f"{scene_id}_"):
                return {
                    "id": f"snap_{scene_id}",
                    "type": "image",
                    "scene_id": scene_id,
                    "path": _rel(project_dir, f),
                    "exists": True,
                    "renderable": True,
                    "snapshot": True,
                }
    except OSError:
        return None
    return None


def _find_script_section(scene: dict, sections: list[dict]) -> Optional[dict]:
    """Join scene → script section by id, falling back to timing overlap."""
    sid = scene.get("script_section_id")
    if sid:
        for s in sections:
            if s.get("id") == sid:
                return s
    start = scene.get("start_seconds")
    end = scene.get("end_seconds")
    if start is None or end is None:
        return None
    best, best_overlap = None, 0.0
    for s in sections:
        s0, s1 = s.get("start_seconds"), s.get("end_seconds")
        if s0 is None or s1 is None:
            continue
        overlap = min(end, s1) - max(start, s0)
        if overlap > best_overlap:
            best, best_overlap = s, overlap
    return best


def _build_storyboard(
    project_dir: Path,
    artifacts: dict[str, dict],
    events: list[dict],
) -> Optional[dict]:
    """Scene cards: scene_plan × script × asset_manifest (+ live events)."""
    scene_plan = artifacts.get("scene_plan")
    if not scene_plan or not isinstance(scene_plan.get("scenes"), list):
        return None
    sections = (artifacts.get("script") or {}).get("sections") or []
    manifest_assets = (artifacts.get("asset_manifest") or {}).get("assets") or []

    def scene_key(value: Any) -> str:
        # 0 is a legitimate scene id — only None/absent collapses to "".
        return str(value) if value is not None else ""

    assets_by_scene: dict[str, list[dict]] = {}
    for asset in manifest_assets:
        if not isinstance(asset, dict):
            continue
        entry = _asset_entry(project_dir, asset)
        assets_by_scene.setdefault(scene_key(entry.get("scene_id")), []).append(entry)

    # A scene is "generating" if its most recent top-level event is an
    # unfinished start. Nested (depth>0) provider events inside a selector
    # call are skipped — the outer call's finish is the real completion.
    generating: dict[str, dict] = {}
    for ev in events:
        sid = ev.get("scene_id")
        if sid is None or ev.get("depth"):
            continue
        sid = scene_key(sid)
        if ev.get("event") == "start":
            generating[sid] = ev
        elif ev.get("event") in ("finish", "error"):
            generating.pop(sid, None)

    cards = []
    for scene in scene_plan["scenes"]:
        if not isinstance(scene, dict):
            continue
        sid = scene_key(scene.get("id"))
        section = _find_script_section(scene, sections)
        scene_assets = assets_by_scene.get(sid, [])
        visuals = [a for a in scene_assets if a["type"] in ("image", "video", "diagram", "animation")]
        audio = [a for a in scene_assets if a["type"] in ("audio", "narration", "music", "sfx")]
        # Only files that can actually be shown (raster/video) are takes; a
        # bespoke composition asset (.tsx animation) is real but not showable.
        renderable = [a for a in visuals if a.get("renderable")]
        # A raster/video asset whose FILE is missing stays as a "file missing"
        # indicator. But an asset that EXISTS yet can't be shown (a .tsx atelier
        # composition) is dropped — it falls back to a per-scene snapshot.
        missing = [a for a in visuals if not a.get("exists") and a["type"] in ("image", "video", "diagram")]
        active_visual = (
            renderable[-1] if renderable
            else missing[-1] if missing
            else _find_scene_snapshot(project_dir, sid)
        )
        cards.append({
            "id": sid,
            "type": scene.get("type"),
            "description": scene.get("description"),
            "start_seconds": scene.get("start_seconds"),
            "end_seconds": scene.get("end_seconds"),
            "duration_seconds": (
                max(0, (scene.get("end_seconds") or 0) - (scene.get("start_seconds") or 0))
                if scene.get("end_seconds") is not None and scene.get("start_seconds") is not None
                else None
            ),
            "hero_moment": bool(scene.get("hero_moment")),
            "shot_language": scene.get("shot_language"),
            "shot_intent": scene.get("shot_intent"),
            "framing": scene.get("framing"),
            "movement": scene.get("movement"),
            "narration": (section or {}).get("text"),
            "section_label": (section or {}).get("label"),
            "required_assets": scene.get("required_assets") or [],
            "visual": active_visual,
            "takes": renderable,
            "audio": audio,
            "generating": generating.get(sid) is not None,
            "generating_tool": (generating.get(sid) or {}).get("tool"),
        })

    total = scene_plan.get("metadata", {}).get("total_duration_seconds")
    if total is None and cards:
        ends = [c["end_seconds"] for c in cards if c["end_seconds"] is not None]
        total = max(ends) if ends else None
    return {
        "scenes": cards,
        "total_duration_seconds": total,
        "style_playbook": scene_plan.get("style_playbook"),
    }


# ---------------------------------------------------------------------------
# Media discovery
# ---------------------------------------------------------------------------

def _scan_media(project_dir: Path) -> dict[str, list[dict]]:
    """Discovered media files (renders, loose assets, snapshots)."""
    renders: list[dict] = []
    snapshots: list[dict] = []
    music: list[dict] = []

    renders_dir = project_dir / "renders"
    if renders_dir.is_dir():
        for f in sorted(renders_dir.iterdir()):
            if f.suffix.lower() in MEDIA_VIDEO_EXT and f.is_file():
                renders.append({"path": _rel(project_dir, f), "size": f.stat().st_size,
                                "mtime": f.stat().st_mtime})
    # Atelier heuristic: deliverables at project root.
    for f in sorted(project_dir.glob("*.mp4")):
        renders.append({"path": _rel(project_dir, f), "size": f.stat().st_size,
                        "mtime": f.stat().st_mtime, "at_root": True})
    for f in sorted(project_dir.glob("*.mp3")):
        music.append({"path": _rel(project_dir, f), "at_root": True})
    music_dir = project_dir / "assets" / "music"
    if music_dir.is_dir():
        for f in sorted(music_dir.iterdir()):
            if f.suffix.lower() in MEDIA_AUDIO_EXT:
                music.append({"path": _rel(project_dir, f)})

    for dirname in ("snapshots", "verify"):
        d = project_dir / dirname
        if d.is_dir():
            for f in sorted(d.iterdir()):
                if f.suffix.lower() in MEDIA_IMAGE_EXT and f.is_file():
                    snapshots.append({"path": _rel(project_dir, f)})

    renders.sort(key=lambda r: r.get("mtime", 0), reverse=True)
    return {"renders": renders, "snapshots": snapshots, "music": music}


def _derive_characters_legacy(project_dir: Path, artifacts: dict) -> list[dict]:
    """Legacy character parser for older character_design / characters.json artifacts."""
    chars: list[dict] = []
    # Source 1: character_design artifact
    cd = artifacts.get("character_design")
    if isinstance(cd, dict) and isinstance(cd.get("characters"), list):
        for item in cd["characters"]:
            cid = item.get("id") or "character"
            chars.append({
                "id": cid,
                "name": item.get("display_name") or item.get("name") or cid.title(),
                "role": item.get("role") or "",
                "age": item.get("age"),
                "style": item.get("style") or item.get("description") or "",
                "props": item.get("props") or [],
                "binding": item.get("binding") or item.get("constraints") or [],
                "image": item.get("image") or item.get("portrait") or item.get("gcs_url"),
                "gcs_url": item.get("gcs_url"),
            })
    # Source 2: characters artifact / file
    if not chars:
        c_json = artifacts.get("characters") or _read_json(project_dir / "artifacts" / "characters.json")
        if isinstance(c_json, dict) and isinstance(c_json.get("characters"), list):
            for item in c_json["characters"]:
                chars.append(item)
    # Source 3: Heuristic scan of clp/ folder
    clp_dir = project_dir / "clp"
    clp_files: dict[str, Path] = {}
    if clp_dir.is_dir():
        for f in clp_dir.iterdir():
            if f.suffix.lower() in MEDIA_IMAGE_EXT and f.is_file():
                clp_files[f.stem.lower()] = f

    # Associate images with characters
    for c in chars:
        if not c.get("image"):
            cid = str(c.get("id", "")).lower()
            cname = str(c.get("name", "")).lower()
            for key in (f"clp_{cid}", cid, f"clp_{cname}", cname):
                if key in clp_files:
                    c["image"] = _rel(project_dir, clp_files[key])
                    break

    # If no chars defined in artifacts, auto-populate from clp directory
    if not chars and clp_files:
        for stem_name, f in sorted(clp_files.items()):
            clean_name = stem_name.replace("clp_", "").replace("_", " ").title()
            chars.append({
                "id": stem_name,
                "name": clean_name,
                "role": "Character",
                "age": None,
                "style": "",
                "props": [],
                "binding": [],
                "image": _rel(project_dir, f),
            })

    # Final pass: check assets/images for matching portraits if still missing
    for c in chars:
        if not c.get("image"):
            cid = str(c.get("id", "")).lower()
            for search_dir in (project_dir / "assets" / "images", project_dir / "output"):
                if search_dir.is_dir():
                    for f in search_dir.glob(f"*{cid}*"):
                        if f.suffix.lower() in MEDIA_IMAGE_EXT and f.is_file():
                            c["image"] = _rel(project_dir, f)
                            break
                if c.get("image"):
                    break

    # GCS Fallback: If local image file doesn't exist on disk, use gcs_url
    for c in chars:
        img = c.get("image")
        if img and not str(img).startswith(("http://", "https://", "//")):
            if not (project_dir / img).is_file() and c.get("gcs_url"):
                c["image"] = c["gcs_url"]
        elif not img and c.get("gcs_url"):
            c["image"] = c["gcs_url"]

    return chars


def _derive_clp(
    project_dir: Path,
    artifacts: dict,
    artifact_diagnostics: Optional[list[dict[str, str]]] = None,
) -> dict[str, list[dict]]:
    """Derive full Character, Location, Prop (CLP) profiles from clp_manifest or legacy sources."""
    clp_data: dict[str, list[dict]] = {
        "characters": [],
        "locations": [],
        "props": [],
    }

    def _resolve_asset_image(item: dict, category: str) -> None:
        raw_img = item.get("image") or item.get("asset_path") or item.get("portrait")
        if raw_img:
            p = project_dir / str(raw_img)
            if p.is_file():
                item["image"] = _rel(project_dir, p)
            elif not str(raw_img).startswith(("http://", "https://", "//")) and item.get("gcs_url"):
                item["image"] = item["gcs_url"]
            else:
                item["image"] = str(raw_img)
        elif item.get("gcs_url"):
            item["image"] = item["gcs_url"]

        if not item.get("image"):
            iid = str(item.get("id", "")).lower()
            iname = str(item.get("name", "")).lower()
            search_dirs = [
                project_dir / "assets" / "clp" / category,
                project_dir / "clp" / category,
                project_dir / "clp",
                project_dir / "assets" / "images",
            ]
            for sdir in search_dirs:
                if sdir.is_dir():
                    for pattern in (f"*{iid}*", f"*{iname}*"):
                        matches = list(sdir.glob(pattern))
                        found = next((m for m in matches if m.suffix.lower() in MEDIA_IMAGE_EXT and m.is_file()), None)
                        if found:
                            item["image"] = _rel(project_dir, found)
                            break
                if item.get("image"):
                    break

        img = item.get("image")
        if img and not str(img).startswith(("http://", "https://", "//")):
            if not (project_dir / img).is_file() and item.get("gcs_url"):
                item["image"] = item["gcs_url"]
        elif not img and item.get("gcs_url"):
            item["image"] = item["gcs_url"]

    # Source 1: only the owning checkpoint's validated CLP artifact. Standalone
    # files are cache copies evaluated by `_collect_artifacts`, never authority.
    manifest = artifacts.get("clp_manifest")
    if isinstance(manifest, dict):
        for cat in ("characters", "locations", "props"):
            entries = manifest.get(cat)
            if isinstance(entries, list):
                for entry in entries:
                    if isinstance(entry, dict):
                        item = dict(entry)
                        _resolve_asset_image(item, cat)
                        clp_data[cat].append(item)
        # If manifest is present, it is authoritative (even if explicitly empty)
        return clp_data

    # A modern standalone CLP file rejected as untrusted/mismatched must not be
    # re-read here or indirectly replaced by a legacy scan. Keep the cabinets
    # empty until a valid owning checkpoint establishes authority.
    if any(
        item.get("artifact") == "clp_manifest"
        for item in (artifact_diagnostics or [])
    ):
        return clp_data

    # Source 2: Legacy fallback
    clp_data["characters"] = _derive_characters_legacy(project_dir, artifacts)

    # Source 3: Heuristic scan of clp/ subdirectories
    for cat in ("characters", "locations", "props"):
        if not clp_data[cat]:
            cat_dir = project_dir / "clp" / cat
            if not cat_dir.is_dir():
                cat_dir = project_dir / "assets" / "clp" / cat
            if cat_dir.is_dir():
                for f in sorted(cat_dir.iterdir()):
                    if f.suffix.lower() in MEDIA_IMAGE_EXT and f.is_file():
                        stem = f.stem.lower()
                        clean_name = stem.replace("clp_", "").replace("_", " ").title()
                        clp_data[cat].append({
                            "id": stem,
                            "name": clean_name,
                            "policy": "strict_reference",
                            "image": _rel(project_dir, f),
                        })

    return clp_data


def _derive_characters(project_dir: Path, artifacts: dict) -> list[dict]:
    """Derive character look profiles (backward compatibility alias)."""
    return _derive_clp(project_dir, artifacts).get("characters", [])


def _find_poster(project_dir: Path, state: dict) -> Optional[str]:
    """Best poster for the library card (image path, or a video path —
    the /thumb endpoint extracts a frame from videos)."""
    board = state.get("storyboard") or {}
    for card in board.get("scenes", []):
        visual = card.get("visual")
        if visual and visual.get("exists") and visual.get("type") == "image":
            return visual["path"]
    for snap in (state.get("media") or {}).get("snapshots", []):
        return snap["path"]
    # Common image homes, in order of how representative they usually are.
    for rel_dir in ("assets/images", "assets/frames", "exports", "assets", "."):
        d = (project_dir / rel_dir) if rel_dir != "." else project_dir
        if not d.is_dir():
            continue
        try:
            for f in sorted(d.iterdir()):
                if f.is_file() and f.suffix.lower() in MEDIA_IMAGE_EXT:
                    return _rel(project_dir, f)
        except OSError:
            continue
    # Last resort: the newest render — /thumb extracts a poster frame.
    renders = (state.get("media") or {}).get("renders", [])
    if renders:
        return renders[0]["path"]
    return None


def _last_activity(project_dir: Path) -> float:
    """Most recent mtime among state-bearing files (bounded scan)."""
    latest = 0.0
    try:
        candidates = list(project_dir.glob("checkpoint_*.json"))
        candidates.append(project_dir / "events.jsonl")
        art = project_dir / "artifacts"
        if art.is_dir():
            candidates.extend(art.glob("*.json"))
        for p in candidates:
            try:
                latest = max(latest, p.stat().st_mtime)
            except OSError:
                continue
    except OSError:
        pass
    return latest


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_board_state(project_dir: Path) -> dict[str, Any]:
    """Full BoardState for one project. Never raises."""
    project_dir = Path(project_dir)
    project_id = project_dir.name

    marker = _read_contained_project_json(
        project_dir, project_dir / "project.json"
    ) or {}
    meta_json = _read_contained_project_json(
        project_dir, project_dir / "meta.json"
    ) or {}

    checkpoints = _collect_checkpoints(project_dir)
    history = _collect_history(project_dir)

    pipeline_type = marker.get("pipeline_type")
    if not pipeline_type:
        for cp in checkpoints.values():
            if cp.get("_checkpoint_invalid"):
                continue
            pt = cp.get("pipeline_type")
            if pt and pt != "unknown":
                pipeline_type = pt
                break
    pipeline_meta = _load_pipeline_meta(pipeline_type)

    artifacts, artifact_diagnostics = _collect_artifacts(project_dir, checkpoints)
    events = read_events(project_dir, limit=250)
    storyboard = _build_storyboard(project_dir, artifacts, events)
    media = _scan_media(project_dir)

    stages = _build_stage_rail(
        pipeline_meta, checkpoints, history, project_dir=project_dir
    )

    # Cost: latest checkpoint snapshot wins; fall back to manifest total.
    cost = None
    # Filesystem freshness is BoardState metadata, not checkpoint payload.
    # Keep it out of the schema-facing envelope and derive it independently.
    checkpoint_items = sorted(
        checkpoints.items(),
        key=lambda item: _checkpoint_mtime(project_dir, item[0]),
        reverse=True,
    )
    for _, cp in checkpoint_items:
        if cp.get("_checkpoint_invalid"):
            continue
        if cp.get("cost_snapshot"):
            cost = cp["cost_snapshot"]
            break
    if cost is None:
        total = (artifacts.get("asset_manifest") or {}).get("total_cost_usd")
        if total is not None:
            cost = {"total_spent_usd": total}

    import time
    last_activity = _last_activity(project_dir)
    now = time.time()

    # Stall detection: an in_progress stage that stopped writing anything.
    for stage_entry in stages:
        if (
            stage_entry["status"] == "in_progress"
            and last_activity
            and (now - last_activity) > STALL_WINDOW_SECONDS
        ):
            stage_entry["stalled"] = True
            stage_entry["stalled_minutes"] = int((now - last_activity) / 60)

    clp_data = _derive_clp(project_dir, artifacts, artifact_diagnostics)
    state: dict[str, Any] = {
        "project_id": project_id,
        "title": marker.get("title") or meta_json.get("name") or project_id.replace("-", " ").title(),
        "pipeline": pipeline_meta,
        "style_playbook": marker.get("style_playbook"),
        "created_at": marker.get("created_at"),
        "has_marker": bool(marker),
        "has_pipeline_state": bool(checkpoints),
        "stages": stages,
        "artifacts": artifacts,
        "artifact_diagnostics": artifact_diagnostics,
        "clp": clp_data,
        "characters": clp_data.get("characters", []),
        "storyboard": storyboard,
        "media": media,
        "events": events,
        "cost": cost,
        "last_activity": last_activity,
        "live": bool(last_activity and (now - last_activity) < LIVE_WINDOW_SECONDS),
    }
    state["poster"] = _find_poster(project_dir, state)
    return state


def summarize_project(project_dir: Path) -> dict[str, Any]:
    """Cheap library-card summary (no full artifact parse of big files)."""
    state = load_board_state(project_dir)
    active = next((s for s in state["stages"] if s["status"] in ("in_progress", "awaiting_human")), None)
    done = [s for s in state["stages"] if s["status"] == "completed"]
    return {
        "project_id": state["project_id"],
        "title": state["title"],
        "pipeline_type": state["pipeline"]["pipeline_type"],
        "has_pipeline_state": state["has_pipeline_state"],
        "poster": state["poster"],
        "live": state["live"],
        "last_activity": state["last_activity"],
        "active_stage": active["name"] if active else None,
        "awaiting_human": bool(active and active["status"] == "awaiting_human"),
        "stage_states": [
            {"name": s["name"], "status": s["status"]}
            for s in state["stages"] if not s.get("undeclared")
        ],
        "completed_count": len(done),
        "render_count": len(state["media"]["renders"]),
        "scene_count": len((state["storyboard"] or {}).get("scenes", [])),
    }


def list_projects(projects_dir: Optional[Path] = None) -> list[dict[str, Any]]:
    """Library view: every project directory, live-first then recency."""
    root = Path(projects_dir) if projects_dir else PROJECTS_DIR
    if not root.is_dir():
        return []
    summaries = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or entry.name.startswith(("_", ".")):
            continue
        try:
            from lib.identity import InvalidProjectIdError, resolve_project_dir

            safe_entry = resolve_project_dir(root, entry.name)
            summaries.append(summarize_project(safe_entry))
        except InvalidProjectIdError:
            # A linked alias is not a project entry, even when Path.is_dir()
            # follows it successfully.
            continue
        except Exception:
            summaries.append({
                "project_id": entry.name,
                "title": entry.name.replace("-", " ").title(),
                "pipeline_type": "unknown",
                "has_pipeline_state": False,
                "poster": None,
                "live": False,
                "last_activity": 0,
                "active_stage": None,
                "awaiting_human": False,
                "stage_states": [],
                "completed_count": 0,
                "render_count": 0,
                "scene_count": 0,
                "error": "unreadable",
            })
    summaries.sort(key=lambda s: (not s["live"], -(s["last_activity"] or 0)))
    return summaries
