from __future__ import annotations


def eye_svg(*, visible: bool, color: str) -> str:
    if visible:
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="3" fill="{color}"/>
  <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z" fill="none" stroke="{color}" stroke-width="2"/>
</svg>
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
  <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z" fill="none" stroke="{color}" stroke-width="2"/>
  <line x1="3" y1="3" x2="21" y2="21" stroke="{color}" stroke-width="2"/>
  <circle cx="12" cy="12" r="3" fill="{color}"/>
</svg>
"""
