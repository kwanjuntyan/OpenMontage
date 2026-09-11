# -*- coding: utf-8 -*-
"""Google Cloud Storage (GCS) client for OpenMontage media assets.

Handles cloud persistence and streaming URLs for:
  1. Rendered videos (final.mp4, scene_*.mp4)
  2. CLP master reference images (shared_clp/)
  3. TTS narration and mix tracks (audio/)

Fails gracefully if GCS_BUCKET_NAME is not configured, allowing seamless
local-only fallback without breaking existing pipelines.
Features thread-safe client initialization, atomic manifest updates,
and bounded background upload workers with graceful exit flush.
"""

from __future__ import annotations

import atexit
import concurrent.futures
import json
import mimetypes
import os
import tempfile
import threading
import urllib.parse
from pathlib import Path
from typing import Optional, Callable, Any

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:
    pass

# Global concurrency governance
_manifest_lock = threading.Lock()
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="gcs-sync")
_pending_futures: set[concurrent.futures.Future] = set()
_futures_lock = threading.Lock()


def _track_future(fut: concurrent.futures.Future):
    with _futures_lock:
        _pending_futures.add(fut)
    fut.add_done_callback(lambda f: _untrack_future(f))


def _untrack_future(fut: concurrent.futures.Future):
    with _futures_lock:
        _pending_futures.discard(fut)


def flush_background_sync(timeout: float = 10.0) -> None:
    """Waits for all in-flight background GCS uploads to finish up to timeout."""
    with _futures_lock:
        current_futures = list(_pending_futures)
    if current_futures:
        concurrent.futures.wait(current_futures, timeout=timeout)


atexit.register(lambda: flush_background_sync(timeout=5.0))


def atomic_update_json(file_path: Path, update_fn: Callable[[dict], bool]) -> bool:
    """Safely updates a JSON file under a process-wide thread lock using atomic replace."""
    with _manifest_lock:
        if not file_path.is_file():
            return False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            changed = update_fn(data)
            if not changed:
                return False

            dir_path = file_path.parent
            dir_path.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("w", dir=str(dir_path), delete=False, encoding="utf-8") as tmp:
                json.dump(data, tmp, indent=2, ensure_ascii=False)
                tmp.flush()
                os.fsync(tmp.fileno())
                temp_name = tmp.name

            os.replace(temp_name, str(file_path))
            return True
        except Exception as e:
            print(f"[GCS Storage] Error in atomic_update_json for {file_path.name}: {e}")
            return False


class GCSStorage:
    """Manages upload and streaming URLs for OpenMontage media assets on GCS."""

    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME", "").strip()
        self._client = None
        self._bucket = None
        self._checked = False
        self._init_lock = threading.Lock()

    def is_configured(self) -> bool:
        """Returns True if GCS bucket name is provided and client can initialize."""
        if not self.bucket_name:
            return False
        with self._init_lock:
            if not self._checked:
                try:
                    from google.cloud import storage
                    gcs_key = os.environ.get("GCS_APPLICATION_CREDENTIALS", "").strip()
                    gcs_proj = os.environ.get("GCS_PROJECT_ID", "").strip() or None

                    if gcs_key and Path(gcs_key).is_file():
                        self._client = storage.Client.from_service_account_json(gcs_key, project=gcs_proj)
                        self._bucket = self._client.bucket(self.bucket_name)
                    else:
                        try:
                            self._client = storage.Client(project=gcs_proj)
                            self._bucket = self._client.bucket(self.bucket_name)
                        except Exception:
                            # Try with default auth if available
                            try:
                                from google.auth import default
                                creds, proj = default()
                                self._client = storage.Client(credentials=creds, project=gcs_proj or proj)
                                self._bucket = self._client.bucket(self.bucket_name)
                            except Exception:
                                pass

                    self._checked = True
                except Exception as e:
                    print(f"[GCS] Initialization notice: {e}")
                    return False
        return self._bucket is not None

    def get_public_url(self, blob_name: str) -> str:
        """Returns standard public storage URL for a given blob name with percent-encoding."""
        encoded_parts = [urllib.parse.quote(part, safe="") for part in blob_name.split("/")]
        return f"https://storage.googleapis.com/{self.bucket_name}/{'/'.join(encoded_parts)}"

    def upload_file(
        self,
        local_path: str | Path,
        destination_blob_name: str,
        content_type: Optional[str] = None,
        make_public: bool = True,
    ) -> Optional[str]:
        """Uploads a local file to GCS and returns its accessible streaming URL."""
        if not self.is_configured():
            return None

        local_file = Path(local_path)
        if not local_file.is_file():
            print(f"[GCS Error] Local file not found: {local_file}")
            return None

        try:
            mime = content_type or mimetypes.guess_type(str(local_file))[0]
            blob = self._bucket.blob(destination_blob_name)

            # Set cache control for streaming media
            if mime and mime.startswith("video/"):
                blob.cache_control = "public, max-age=31536000"
            elif mime and mime.startswith("image/"):
                blob.cache_control = "public, max-age=86400"

            blob.upload_from_filename(str(local_file), content_type=mime)

            if make_public:
                try:
                    blob.make_public()
                except Exception:
                    # Uniform bucket-level access handles access via bucket IAM
                    pass

            public_url = self.get_public_url(destination_blob_name)
            print(f"[GCS] Uploaded: {destination_blob_name} -> {public_url}")
            return public_url

        except Exception as e:
            print(f"[GCS Upload Failed] {destination_blob_name}: {e}")
            return None

    def upload_asset(
        self,
        project_id: str,
        local_path: str | Path,
        rel_path: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> Optional[str]:
        """Unified upload method for all media types (CLP, video, audio, image, render)."""
        local_file = Path(local_path)
        if not local_file.is_file():
            return None

        # Determine relative path inside project if not explicitly given
        if not rel_path:
            p_parts = local_file.parts
            if "projects" in p_parts:
                idx = p_parts.index("projects")
                rel_parts = p_parts[idx + 2:]
                rel_path = "/".join(rel_parts)
            else:
                rel_path = local_file.name

        rel_path = rel_path.replace("\\", "/")
        destination_blob = f"projects/{project_id}/{rel_path}"
        return self.upload_file(local_file, destination_blob, content_type=content_type)

    def upload_clp(self, filename: str, local_path: str | Path) -> Optional[str]:
        """Uploads character portrait image to GCS shared_clp/ directory."""
        destination_blob = f"shared_clp/{filename}"
        return self.upload_file(local_path, destination_blob, content_type="image/jpeg")

    def sync_project_assets(self, project_dir: str | Path) -> dict[str, str]:
        """Scans project directory and uploads all local media assets to GCS."""
        if not self.is_configured():
            return {}

        p_dir = Path(project_dir)
        if not p_dir.is_dir():
            return {}

        project_id = p_dir.name
        results: dict[str, str] = {}

        targets = [
            (p_dir / "assets" / "clp", "assets/clp", "image/jpeg"),
            (p_dir / "assets" / "video", "assets/video", "video/mp4"),
            (p_dir / "assets" / "images", "assets/images", "image/jpeg"),
            (p_dir / "assets" / "audio", "assets/audio", "audio/mpeg"),
            (p_dir / "renders", "renders", "video/mp4"),
            (p_dir / "clp", "clp", "image/jpeg"),
        ]

        for folder, rel_prefix, mime in targets:
            if folder.is_dir():
                for f in folder.iterdir():
                    if f.is_file() and not f.name.startswith("."):
                        rel_path = f"{rel_prefix}/{f.name}".replace("\\", "/")
                        url = self.upload_asset(project_id, f, rel_path=rel_path, content_type=mime)
                        if url:
                            results[rel_path] = url
                            if rel_prefix == "clp":
                                self.upload_clp(f.name, f)

        # 1. Update artifacts/asset_manifest.json with atomic lock
        manifest_path = p_dir / "artifacts" / "asset_manifest.json"
        if manifest_path.is_file() and results:
            def _update_manifest(manifest: dict) -> bool:
                changed = False
                for asset in manifest.get("assets", []):
                    ap = asset.get("path", "").replace("\\", "/")
                    fn = Path(ap).name
                    matched_url = results.get(ap)
                    if not matched_url:
                        for r_path, url in results.items():
                            if r_path.endswith(f"/{fn}") or r_path == fn:
                                matched_url = url
                                break
                    if matched_url and asset.get("gcs_url") != matched_url:
                        asset["gcs_url"] = matched_url
                        changed = True
                return changed

            atomic_update_json(manifest_path, _update_manifest)

        # 2. Update artifacts/character_design.json with atomic lock
        cd_path = p_dir / "artifacts" / "character_design.json"
        if cd_path.is_file() and results:
            def _update_cd(cd_data: dict) -> bool:
                changed = False
                for char in cd_data.get("characters", []):
                    img_name = Path(char.get("image", "")).name
                    matched_url = None
                    for r_path, url in results.items():
                        if r_path.endswith(f"/{img_name}") or r_path == img_name or char.get("id") in r_path:
                            matched_url = url
                            break
                    if matched_url and char.get("gcs_url") != matched_url:
                        char["gcs_url"] = matched_url
                        changed = True
                return changed

            atomic_update_json(cd_path, _update_cd)

        # 3. Update artifacts/render_report.json and project.json
        render_url = results.get("renders/final.mp4")
        if render_url:
            rep_path = p_dir / "artifacts" / "render_report.json"
            if rep_path.is_file():
                def _update_rep(rep: dict) -> bool:
                    if rep.get("gcs_url") != render_url:
                        rep["gcs_url"] = render_url
                        return True
                    return False
                atomic_update_json(rep_path, _update_rep)

            pj_path = p_dir / "project.json"
            if pj_path.is_file():
                def _update_pj(pj: dict) -> bool:
                    if pj.get("gcs_url") != render_url:
                        pj["gcs_url"] = render_url
                        return True
                    return False
                atomic_update_json(pj_path, _update_pj)

        return results

    def sync_project_clp(self, project_dir: str | Path) -> dict[str, str]:
        """Backward-compatible alias: uploads CLP images and updates character_design.json."""
        return self.sync_project_assets(project_dir)

    def is_auto_sync_enabled(self) -> bool:
        """Checks if GCS auto-sync is enabled (default: true if bucket is configured)."""
        val = os.environ.get("GCS_AUTO_SYNC", "true").strip().lower()
        if val in ("0", "false", "no", "off"):
            return False
        return self.is_configured()

    def async_sync_project_assets(
        self,
        project_dir: str | Path,
        on_complete: Optional[Callable[[dict[str, str]], None]] = None,
    ) -> Optional[concurrent.futures.Future]:
        """Executes sync_project_assets in a bounded ThreadPoolExecutor worker."""
        if not self.is_auto_sync_enabled():
            return None

        p_dir = Path(project_dir)

        def _task():
            try:
                res = self.sync_project_assets(p_dir)
                if on_complete and callable(on_complete):
                    on_complete(res)
                return res
            except Exception as e:
                print(f"[GCS Auto-Sync] Background sync error for {p_dir.name}: {e}")
                return {}

        fut = _executor.submit(_task)
        _track_future(fut)
        return fut

    def async_upload_single_asset(
        self,
        project_id: str,
        local_path: str | Path,
        rel_path: Optional[str] = None,
    ) -> Optional[concurrent.futures.Future]:
        """Uploads a single asset asynchronously in a bounded worker and updates manifest."""
        if not self.is_auto_sync_enabled():
            return None

        local_file = Path(local_path)
        if not local_file.is_file():
            return None

        def _task():
            try:
                url = self.upload_asset(project_id, local_file, rel_path=rel_path)
                if not url:
                    return None

                from lib.paths import PROJECTS_DIR
                p_dir = PROJECTS_DIR / project_id
                manifest_path = p_dir / "artifacts" / "asset_manifest.json"
                if manifest_path.is_file():
                    fn = local_file.name
                    def _update_manifest(manifest: dict) -> bool:
                        changed = False
                        for asset in manifest.get("assets", []):
                            ap = asset.get("path", "").replace("\\", "/")
                            if ap.endswith(f"/{fn}") or ap == fn or (rel_path and ap == rel_path):
                                if asset.get("gcs_url") != url:
                                    asset["gcs_url"] = url
                                    changed = True
                        return changed

                    atomic_update_json(manifest_path, _update_manifest)
                return url
            except Exception as e:
                print(f"[GCS Auto-Sync] Single asset background upload notice: {e}")
                return None

        fut = _executor.submit(_task)
        _track_future(fut)
        return fut


# Singleton instance for import throughout OpenMontage
gcs_storage = GCSStorage()
