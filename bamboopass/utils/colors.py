from __future__ import annotations

from dataclasses import dataclass


def _clamp_u8(x: float) -> int:
    return max(0, min(255, int(round(x))))


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def c_lum(c: int) -> float:
        x = c / 255.0
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * c_lum(r) + 0.7152 * c_lum(g) + 0.0722 * c_lum(b)


def contrast_ratio(rgb1: tuple[int, int, int], rgb2: tuple[int, int, int]) -> float:
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


@dataclass(frozen=True)
class TextColors:
    primary: str
    secondary: str


def best_text_colors(bg_hex: str) -> TextColors:
    """Return (primary, secondary) text colors for a background.

    Prefers WCAG-ish contrast; falls back to luminance if both white/black fail.
    """
    bg = hex_to_rgb(bg_hex)
    white = (255, 255, 255)
    black = (0, 0, 0)

    if contrast_ratio(bg, white) >= 4.5:
        main = white
    elif contrast_ratio(bg, black) >= 4.5:
        main = black
    else:
        main = white if relative_luminance(bg) < 0.5 else black

    # secondary: blend main towards background for subtler placeholder text
    factor = 0.6
    r, g, b = main
    sr = _clamp_u8(r + (bg[0] - r) * factor)
    sg = _clamp_u8(g + (bg[1] - g) * factor)
    sb = _clamp_u8(b + (bg[2] - b) * factor)
    return TextColors(primary=rgb_to_hex(main), secondary=rgb_to_hex((sr, sg, sb)))
