# -*- coding: utf-8 -*-
"""Google Cloud Storage (GCS) client for OpenMontage media assets.

Handles cloud persistence and streaming URLs for:
  1. Rendered videos (final.mp4, scene_*.mp4)
  2. CLP master reference images (shared_clp/)
  3. TTS narration and mix tracks (audio/)

Fails gracefully if GCS_BUCKET_NAME is not configured, allowing seamless
local-only fallback without breaking existing pipelines.
"""

from __future__ import annotations

import os
import mimetypes
import threading
from pathlib import Path
from typing import Optional, Callable

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:
    pass


class GCSStorage:
    """Manages upload and streaming URLs for OpenMontage media assets on GCS."""

    def __init__(self, bucket_name: Optional[str] = None):
        self.bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME", "").strip()
        self._client = None
        self._bucket = None
        self._checked = False

    def is_configured(self) -> bool:
        """Returns True if GCS bucket name is provided and client can initialize."""
        if not self.bucket_name:
            return False
        if not self._checked:
            try:
                from google.cloud import storage
                gcs_key = os.environ.get("GCS_APPLICATION_CREDENTIALS", "").strip()
                gcs_proj = os.environ.get("GCS_PROJECT_ID", "").strip() or None

                if gcs_key and Path(gcs_key).is_file():
                    self._client = storage.Client.from_service_account_json(gcs_key, project=gcs_proj)
                    self._bucket = self._client.bucket(self.bucket_name)
                else:
                    # Try standard client; if 403 occurs (e.g. GOOGLE_APPLICATION_CREDENTIALS is a Vertex-only key),
                    # fallback to Application Default Credentials (ADC).
                    try:
                        self._client = storage.Client(project=gcs_proj)
                        self._bucket = self._client.bucket(self.bucket_name)
                        # Quick probe
                        self._bucket.exists()
                    except Exception:
                        from google.auth import default
                        orig_key = os.environ.pop("GOOGLE_APPLICATION_CREDENTIALS", None)
                        try:
                            creds, proj = default()
                            self._client = storage.Client(credentials=creds, project=gcs_proj or proj)
                            self._bucket = self._client.bucket(self.bucket_name)
                        finally:
                            if orig_key:
                                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = orig_key

                self._checked = True
            except Exception as e:
                print(f"[GCS] Initialization notice: {e}")
                return False
        return self._bucket is not None

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
                    # Uniform bucket-level access might forbid per-object ACLs;
                    # In that case bucket IAM policy handles public access.
                    pass

            public_url = f"https://storage.googleapis.com/{self.bucket_name}/{destination_blob_name}"
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
        """Unified upload method for all media types (CLP, video, audio, image, render).

        Maps local project asset directly to projects/<project_id>/<rel_path> on GCS.
        """
        local_file = Path(local_path)
        if not local_file.is_file():
            print(f"[GCS Error] Local asset not found: {local_file}")
            return None

        # Determine relative destination blob path
        if rel_path:
            clean_rel = rel_path.replace("\\", "/").lstrip("/")
            blob_path = f"projects/{project_id}/{clean_rel}"
        else:
            # Auto-detect from file extension and parent directory
            ext = local_file.suffix.lower()
            parent_name = local_file.parent.name.lower()
            if "clp" in parent_name:
                blob_path = f"projects/{project_id}/clp/{local_file.name}"
            elif ext in {".mp4", ".webm", ".mov"}:
                if "render" in parent_name or local_file.name == "final.mp4":
                    blob_path = f"projects/{project_id}/renders/{local_file.name}"
                else:
                    blob_path = f"projects/{project_id}/assets/video/{local_file.name}"
            elif ext in {".mp3", ".wav", ".m4a", ".aac", ".ogg"}:
                blob_path = f"projects/{project_id}/assets/audio/{local_file.name}"
            elif ext in {".png", ".jpg", ".jpeg", ".webp"}:
                blob_path = f"projects/{project_id}/assets/images/{local_file.name}"
            else:
                blob_path = f"projects/{project_id}/assets/{local_file.name}"

        return self.upload_file(local_file, blob_path, content_type=content_type)

    def upload_render(self, project_id: str, local_mp4_path: str | Path) -> Optional[str]:
        """Uploads final or scene MP4 to projects/<project_id>/renders/<filename>."""
        filename = Path(local_mp4_path).name
        return self.upload_asset(project_id, local_mp4_path, rel_path=f"renders/{filename}", content_type="video/mp4")

    def upload_clp(self, clp_name: str, local_image_path: str | Path) -> Optional[str]:
        """Uploads CLP reference prop/character to shared_clp/<clp_name>.<ext>."""
        ext = Path(local_image_path).suffix or ".png"
        clean_name = clp_name
        if clean_name.endswith(ext):
            clean_name = clean_name[:-len(ext)]
        blob_path = f"shared_clp/{clean_name}{ext}"
        return self.upload_file(local_image_path, blob_path)

    def upload_audio(self, project_id: str, local_audio_path: str | Path) -> Optional[str]:
        """Uploads narration/mix audio to projects/<project_id>/assets/audio/<filename>."""
        filename = Path(local_audio_path).name
        return self.upload_asset(project_id, local_audio_path, rel_path=f"assets/audio/{filename}", content_type="audio/mpeg")

    def sync_project_assets(self, project_dir: str | Path) -> dict[str, str]:
        """Unified sync of ALL project media assets (CLP, shot video, audio, image, render) to GCS.

        Scans:
          - clp/
          - assets/video/
          - assets/images/
          - assets/audio/
          - renders/
        Uploads each file to GCS and automatically updates:
          - artifacts/asset_manifest.json (with gcs_url per asset)
          - artifacts/character_design.json (with gcs_url per character)
          - artifacts/render_report.json & project.json (with gcs_url for renders)
        """
        p_dir = Path(project_dir)
        project_id = p_dir.name
        results: dict[str, str] = {}
        if not self.is_configured():
            print(f"[GCS] Bucket not configured, skipping sync for {project_id}.")
            return results

        # Directories to scan and their relative subpaths
        scan_targets = [
            ("clp", p_dir / "clp"),
            ("assets/video", p_dir / "assets" / "video"),
            ("assets/images", p_dir / "assets" / "images"),
            ("assets/audio", p_dir / "assets" / "audio"),
            ("renders", p_dir / "renders"),
        ]

        valid_exts = {
            ".mp4", ".webm", ".mov",
            ".mp3", ".wav", ".m4a", ".aac",
            ".png", ".jpg", ".jpeg", ".webp"
        }

        for rel_prefix, target_dir in scan_targets:
            if not target_dir.is_dir():
                continue
            for f in sorted(target_dir.iterdir()):
                if f.is_file() and f.suffix.lower() in valid_exts:
                    rel_path = f"{rel_prefix}/{f.name}"
                    url = self.upload_asset(project_id, f, rel_path=rel_path)
                    if url:
                        results[rel_path] = url
                        # Also upload CLP to shared_clp for global cross-project sharing
                        if rel_prefix == "clp":
                            self.upload_clp(f.name, f)

        import json

        # 1. Update artifacts/asset_manifest.json
        manifest_path = p_dir / "artifacts" / "asset_manifest.json"
        if manifest_path.is_file() and results:
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                changed = False
                for asset in manifest.get("assets", []):
                    asset_path = asset.get("path", "").replace("\\", "/")
                    filename = Path(asset_path).name
                    # Try matching by exact relative path or filename
                    matched_url = None
                    if asset_path in results:
                        matched_url = results[asset_path]
                    else:
                        for r_path, url in results.items():
                            if r_path.endswith(f"/{filename}") or r_path == filename:
                                matched_url = url
                                break
                    if matched_url and asset.get("gcs_url") != matched_url:
                        asset["gcs_url"] = matched_url
                        changed = True

                if changed:
                    with open(manifest_path, "w", encoding="utf-8") as f:
                        json.dump(manifest, f, indent=2, ensure_ascii=False)
                    print(f"[GCS] Updated {manifest_path.name} with asset GCS URLs.")
            except Exception as e:
                print(f"[GCS] Error updating asset_manifest.json: {e}")

        # 2. Update artifacts/character_design.json
        cd_path = p_dir / "artifacts" / "character_design.json"
        if cd_path.is_file() and results:
            try:
                with open(cd_path, "r", encoding="utf-8") as f:
                    cd_data = json.load(f)
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

                if changed:
                    with open(cd_path, "w", encoding="utf-8") as f:
                        json.dump(cd_data, f, indent=2, ensure_ascii=False)
                    print(f"[GCS] Updated {cd_path.name} with character GCS URLs.")
            except Exception as e:
                print(f"[GCS] Error updating character_design.json: {e}")

        # 3. Update artifacts/render_report.json and project.json
        render_url = results.get("renders/final.mp4")
        if render_url:
            rep_path = p_dir / "artifacts" / "render_report.json"
            if rep_path.is_file():
                try:
                    with open(rep_path, "r", encoding="utf-8") as f:
                        rep = json.load(f)
                    rep["gcs_url"] = render_url
                    with open(rep_path, "w", encoding="utf-8") as f:
                        json.dump(rep, f, indent=2, ensure_ascii=False)
                except Exception:
                    pass
            pj_path = p_dir / "project.json"
            if pj_path.is_file():
                try:
                    with open(pj_path, "r", encoding="utf-8") as f:
                        pj = json.load(f)
                    pj["gcs_url"] = render_url
                    with open(pj_path, "w", encoding="utf-8") as f:
                        json.dump(pj, f, indent=2, ensure_ascii=False)
                except Exception:
                    pass

        return results

    def sync_project_clp(self, project_dir: str | Path) -> dict[str, str]:
        """Backward-compatible alias: uploads CLP images and updates character_design.json."""
        return self.sync_project_assets(project_dir)

    def get_public_url(self, blob_name: str) -> str:
        """Returns standard public storage URL for a given blob name."""
        return f"https://storage.googleapis.com/{self.bucket_name}/{blob_name}"

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
    ) -> Optional[threading.Thread]:
        """Executes sync_project_assets in a background daemon thread."""
        if not self.is_auto_sync_enabled():
            return None

        p_dir = Path(project_dir)

        def _worker():
            try:
                results = self.sync_project_assets(p_dir)
                if on_complete and callable(on_complete):
                    on_complete(results)
            except Exception as e:
                print(f"[GCS Auto-Sync] Background sync error for {p_dir.name}: {e}")

        t = threading.Thread(target=_worker, name=f"gcs-sync-{p_dir.name}", daemon=True)
        t.start()
        return t

    def async_upload_single_asset(
        self,
        project_id: str,
        local_path: str | Path,
        rel_path: Optional[str] = None,
    ) -> Optional[threading.Thread]:
        """Uploads a single asset asynchronously in a daemon thread and updates manifest."""
        if not self.is_auto_sync_enabled():
            return None

        local_file = Path(local_path)
        if not local_file.is_file():
            return None

        def _worker():
            try:
                url = self.upload_asset(project_id, local_file, rel_path=rel_path)
                if not url:
                    return
                # Update manifest if project dir can be resolved
                from lib.paths import PROJECTS_DIR
                p_dir = PROJECTS_DIR / project_id
                manifest_path = p_dir / "artifacts" / "asset_manifest.json"
                if manifest_path.is_file():
                    import json
                    filename = local_file.name
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    changed = False
                    for asset in manifest.get("assets", []):
                        ap = asset.get("path", "").replace("\\", "/")
                        if ap.endswith(f"/{filename}") or ap == filename or (rel_path and ap == rel_path):
                            if asset.get("gcs_url") != url:
                                asset["gcs_url"] = url
                                changed = True
                    if changed:
                        with open(manifest_path, "w", encoding="utf-8") as f:
                            json.dump(manifest, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[GCS Auto-Sync] Single asset background upload notice: {e}")

        t = threading.Thread(target=_worker, name=f"gcs-upload-{local_file.name}", daemon=True)
        t.start()
        return t


# Singleton instance for import throughout OpenMontage
gcs_storage = GCSStorage()
