"""Version helpers.

We intentionally do not hardcode a release version in source code.
For tagged builds, CI writes bamboopass/_build_version.py using the tag value.
"""

from __future__ import annotations


def get_version(dist_name: str = "bamboopass") -> str:
    # 1) CI-injected build version (tag builds / frozen binaries)
    try:
        from ._build_version import __version__ as _build_version  # type: ignore
        if _build_version and _build_version != "0.0.0-dev":
            return _build_version
    except Exception:
        pass

    # 2) Installed package metadata (pip/aur)
    try:
        from importlib.metadata import version as _version  # py>=3.8
        v = _version(dist_name)
        if v:
            return v
    except Exception:
        pass

    return "0.0.0-dev"


__version__ = get_version()
