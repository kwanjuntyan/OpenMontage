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
from pathlib import Path
from typing import Optional

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
                self._client = storage.Client()
                self._bucket = self._client.bucket(self.bucket_name)
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

    def upload_render(self, project_id: str, local_mp4_path: str | Path) -> Optional[str]:
        """Uploads final or scene MP4 to projects/<project_id>/renders/<filename>."""
        filename = Path(local_mp4_path).name
        blob_path = f"projects/{project_id}/renders/{filename}"
        return self.upload_file(local_mp4_path, blob_path, content_type="video/mp4")

    def upload_clp(self, clp_name: str, local_image_path: str | Path) -> Optional[str]:
        """Uploads CLP reference prop/character to shared_clp/<clp_name>.<ext>."""
        ext = Path(local_image_path).suffix or ".png"
        clean_name = clp_name
        if clean_name.endswith(ext):
            clean_name = clean_name[:-len(ext)]
        blob_path = f"shared_clp/{clean_name}{ext}"
        return self.upload_file(local_image_path, blob_path)

    def sync_project_clp(self, project_dir: str | Path) -> dict[str, str]:
        """Uploads all CLP images in a project's clp/ folder and updates character_design.json."""
        p_dir = Path(project_dir)
        results: dict[str, str] = {}
        if not self.is_configured():
            print("[GCS] Bucket not configured, skipping CLP sync.")
            return results

        # 1. Upload files from clp/ directory
        clp_dir = p_dir / "clp"
        if clp_dir.is_dir():
            for img_file in clp_dir.iterdir():
                if img_file.is_file() and img_file.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                    url = self.upload_clp(img_file.name, img_file)
                    if url:
                        results[img_file.name] = url

        # 2. Update character_design.json if it exists
        cd_path = p_dir / "artifacts" / "character_design.json"
        if cd_path.is_file() and results:
            try:
                import json
                with open(cd_path, "r", encoding="utf-8") as f:
                    cd_data = json.load(f)

                changed = False
                for char in cd_data.get("characters", []):
                    img_name = Path(char.get("image", "")).name
                    if img_name in results:
                        char["gcs_url"] = results[img_name]
                        changed = True
                    elif f"clp_{char.get('id')}.jpg" in results:
                        char["gcs_url"] = results[f"clp_{char.get('id')}.jpg"]
                        changed = True
                    elif f"clp_{char.get('id')}.png" in results:
                        char["gcs_url"] = results[f"clp_{char.get('id')}.png"]
                        changed = True

                if changed:
                    with open(cd_path, "w", encoding="utf-8") as f:
                        json.dump(cd_data, f, indent=2, ensure_ascii=False)
                    print(f"[GCS] Updated {cd_path.name} with CLP GCS URLs.")
            except Exception as e:
                print(f"[GCS] Error updating character_design.json: {e}")

        return results

    def upload_audio(self, project_id: str, local_audio_path: str | Path) -> Optional[str]:
        """Uploads narration/mix audio to projects/<project_id>/audio/<filename>."""
        filename = Path(local_audio_path).name
        blob_path = f"projects/{project_id}/audio/{filename}"
        return self.upload_file(local_audio_path, blob_path, content_type="audio/mpeg")

    def get_public_url(self, blob_name: str) -> str:
        """Returns standard public storage URL for a given blob name."""
        return f"https://storage.googleapis.com/{self.bucket_name}/{blob_name}"


# Singleton instance for import throughout OpenMontage
gcs_storage = GCSStorage()
