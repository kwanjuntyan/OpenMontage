"""Theme-driven text must stay legible on light playbooks.

Three of the five shipped playbooks are light-background (clean-professional,
minimalist-diagram, premium-minimalist), but several Remotion components render
near-white text unconditionally. The worst case is the burned-in captions:
Explainer handed CaptionOverlay a light `captionBackgroundColor` while leaving
the word color at its `#F8FAFC` default, which is 1.05:1 — invisible.

The wiring assertions follow the source-text idiom already used by
test_remotion_video_transition_contract.py; the contrast assertion checks the
values that wiring actually delivers.
"""

import re
from copy import deepcopy
from pathlib import Path

import pytest

from styles.playbook_loader import list_playbooks, load_playbook, validate_contrast
from tools.video.video_compose import VideoCompose

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPOSER = REPO_ROOT / "remotion-composer" / "src"

# WCAG 2.1 AA for normal-size text.
MIN_CONTRAST = 4.5
LIGHT_CAPTION_BAR = "rgba(255, 255, 255, 0.85)"
DARK_CAPTION_BAR = "rgba(15, 23, 42, 0.75)"


def _read(relative: str) -> str:
    return (COMPOSER / relative).read_text(encoding="utf-8")


def _to_rgba(color: str) -> tuple[float, float, float, float]:
    color = color.strip()
    if color.startswith("#"):
        hex_digits = color[1:]
        if len(hex_digits) == 3:
            hex_digits = "".join(c * 2 for c in hex_digits)
        r, g, b = (int(hex_digits[i : i + 2], 16) for i in (0, 2, 4))
        return (r, g, b, 1.0)
    match = re.match(r"rgba?\(([^)]+)\)", color)
    if not match:
        raise ValueError(f"unparseable color: {color!r}")
    parts = [float(p) for p in match.group(1).split(",")]
    alpha = parts[3] if len(parts) > 3 else 1.0
    return (parts[0], parts[1], parts[2], alpha)


def _composite(foreground: str, backdrop: str) -> str:
    """Flatten a possibly-translucent color over an opaque one, as the GPU would."""
    fr, fg, fb, alpha = _to_rgba(foreground)
    br, bg, bb, _ = _to_rgba(backdrop)
    blended = (
        round(alpha * fr + (1 - alpha) * br),
        round(alpha * fg + (1 - alpha) * bg),
        round(alpha * fb + (1 - alpha) * bb),
    )
    return "#%02X%02X%02X" % blended


def _theme_for_custom_palette(monkeypatch, *, background: str, text: str) -> dict:
    playbook = deepcopy(load_playbook("clean-professional"))
    palette = playbook["visual_language"]["color_palette"]
    palette["background"] = background
    palette["text"] = text
    monkeypatch.setattr(
        "styles.playbook_loader.load_playbook",
        lambda _name: playbook,
    )
    theme = VideoCompose()._build_theme_from_playbook("custom", {})
    assert theme is not None
    return theme


def test_explainer_gives_captions_the_theme_text_color() -> None:
    """Regression: the caption word color was left at CaptionOverlay's dark-theme default."""
    source = _read("Explainer.tsx")

    caption_call = source[source.index("<CaptionOverlay") :]
    caption_call = caption_call[: caption_call.index("/>")]

    assert "color={theme.textColor}" in caption_call
    assert "highlightColor={theme.captionHighlightColor}" in caption_call
    assert "backgroundColor={theme.captionBackgroundColor}" in caption_call


def test_overlay_renderer_receives_the_theme() -> None:
    """OverlayRenderer had no access to the theme at all, so overlays could not follow it."""
    source = _read("Explainer.tsx")

    assert "OverlayRenderer: React.FC<{ overlay: Overlay; theme: ThemeConfig }>" in source
    assert "<OverlayRenderer overlay={overlay} theme={theme} />" in source


@pytest.mark.parametrize("component", ["SectionTitle", "StatReveal", "HeroTitle"])
def test_theme_text_color_is_threaded_into_overlay_components(component: str) -> None:
    source = _read("Explainer.tsx")

    call = source[source.index(f"<{component}") :]
    call = call[: call.index("/>")]
    assert "textColor=" in call, f"<{component}> is not given a text color"


@pytest.mark.parametrize(
    ("component", "expected"),
    [
        ("components/SectionTitle.tsx", "color: textColor,"),
        ("components/StatReveal.tsx", "color: textColor,"),
        ("components/HeroTitle.tsx", "color: i < 8 ? accentColor : textColor,"),
        ("components/HeroTitle.tsx", "color: subtitleColor,"),
        ("components/HeroTitle.tsx", "backgroundColor: accentColor,"),
        ("components/HeroTitle.tsx", "background: scrimBackground,"),
    ],
)
def test_components_render_from_props_not_literals(component: str, expected: str) -> None:
    """The palette may survive as default parameter values, but not inline in the JSX."""
    assert expected in _read(component)


def test_hero_scrim_flips_with_theme_lightness() -> None:
    """A dark scrim under a light theme's dark title drops the pair to ~3.4:1."""
    source = _read("Explainer.tsx")

    scrim = source[source.index("function heroScrim") :]
    scrim = scrim[: scrim.index("\n}")]
    assert "isLightColor(theme.backgroundColor)" in scrim
    assert '"#FFFFFF"' in scrim
    assert '"#0F172A"' in scrim


@pytest.mark.parametrize("playbook", sorted(list_playbooks()))
def test_every_playbook_theme_keeps_captions_legible(playbook: str) -> None:
    """The color the wiring delivers must actually pass AA against the caption bar."""
    theme = VideoCompose()._build_theme_from_playbook(playbook, {})
    if not theme:
        pytest.skip(f"{playbook} does not currently yield a theme")

    caption_bar = _composite(theme["captionBackgroundColor"], theme["backgroundColor"])
    ratio = validate_contrast(theme["textColor"], caption_bar)["ratio"]

    assert ratio >= MIN_CONTRAST, (
        f"{playbook}: caption text {theme['textColor']} on bar {caption_bar} "
        f"is {ratio}:1, below WCAG AA {MIN_CONTRAST}:1"
    )


@pytest.mark.parametrize(
    ("background", "text", "expected_bar"),
    [
        ("#F5F4EF", "#121212", LIGHT_CAPTION_BAR),
        ("#101827", "#F8FAFC", DARK_CAPTION_BAR),
    ],
)
def test_custom_palette_selects_the_highest_contrast_caption_bar(
    monkeypatch,
    background: str,
    text: str,
    expected_bar: str,
) -> None:
    theme = _theme_for_custom_palette(
        monkeypatch,
        background=background,
        text=text,
    )

    ratios = {
        candidate: validate_contrast(text, _composite(candidate, background))["ratio"]
        for candidate in (LIGHT_CAPTION_BAR, DARK_CAPTION_BAR)
    }
    assert theme["captionBackgroundColor"] == expected_bar
    assert ratios[expected_bar] == max(ratios.values())


@pytest.mark.parametrize(
    ("text", "expected_bar"),
    [
        ("#121212", LIGHT_CAPTION_BAR),
        ("#F8FAFC", DARK_CAPTION_BAR),
    ],
)
def test_invalid_background_uses_best_worst_case_caption_bar(
    monkeypatch,
    text: str,
    expected_bar: str,
) -> None:
    theme = _theme_for_custom_palette(
        monkeypatch,
        background="paper-white",
        text=text,
    )

    worst_case_ratios = {
        candidate: min(
            validate_contrast(text, _composite(candidate, backdrop))["ratio"]
            for backdrop in ("#000000", "#FFFFFF")
        )
        for candidate in (LIGHT_CAPTION_BAR, DARK_CAPTION_BAR)
    }
    assert theme["captionBackgroundColor"] == expected_bar
    assert worst_case_ratios[expected_bar] == max(worst_case_ratios.values())


def test_invalid_text_uses_fixed_dark_caption_fallback(monkeypatch) -> None:
    theme = _theme_for_custom_palette(
        monkeypatch,
        background="#F5F4EF",
        text="editorial-ink",
    )

    assert theme["captionBackgroundColor"] == DARK_CAPTION_BAR
