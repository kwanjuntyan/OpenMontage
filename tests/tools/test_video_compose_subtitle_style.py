"""Subtitle-style resolution must accept the canonical edit schema."""

from schemas.artifacts import validate_artifact
from tools.video.video_compose import VideoCompose


def test_schema_string_style_is_not_treated_as_visual_style_mapping():
    edit_decisions = {
        "version": "1.0",
        "render_runtime": "ffmpeg",
        "cuts": [
            {
                "id": "cut-1",
                "source": "fixture.mp4",
                "in_seconds": 0,
                "out_seconds": 1,
            }
        ],
        "subtitles": {
            "enabled": True,
            "style": "sentence",
            "font": "Atkinson Hyperlegible",
            "font_size": 34,
            "color": "&H00F0F0F0",
            "outline_color": "&H00101010",
            "background": "&H80000000",
            "position": "top-center",
        },
    }
    validate_artifact("edit_decisions", edit_decisions)
    resolved = VideoCompose._resolve_subtitle_style(
        explicit_style=None,
        edit_decisions=edit_decisions,
        playbook=None,
    )

    assert resolved["font"] == "Atkinson Hyperlegible"
    assert resolved["font_size"] == 34
    assert resolved["primary_color"] == "&H00F0F0F0"
    assert resolved["outline_color"] == "&H00101010"
    assert resolved["back_color"] == "&H80000000"
    assert resolved["alignment"] == 8
    assert "style" not in resolved


def test_legacy_mapping_style_remains_a_bounded_compatibility_input():
    resolved = VideoCompose._resolve_subtitle_style(
        explicit_style=None,
        edit_decisions={
            "subtitles": {
                "style": {
                    "font": "Legacy Font",
                    "font_size": 30,
                    "primary_color": "&H00FFFFFF",
                    "not_a_visual_style_key": "ignored",
                }
            }
        },
        playbook=None,
    )

    assert resolved["font"] == "Legacy Font"
    assert resolved["font_size"] == 30
    assert resolved["primary_color"] == "&H00FFFFFF"
    assert "not_a_visual_style_key" not in resolved
