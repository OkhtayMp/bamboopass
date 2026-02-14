from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from platformdirs import user_cache_dir

from .constants import APP_NAME


@dataclass
class Settings:
    bg_color: str = "#FFFFFF"
    iterations: int = 200_000
    password_length: int = 30
    clipboard_check_interval_ms: int = 100

    @classmethod
    def load(cls) -> Settings:
        path = settings_file()
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return cls(
                bg_color=str(data.get("bg_color", cls.bg_color)),
                iterations=int(data.get("iterations", cls.iterations)),
                password_length=int(data.get("password_length", cls.password_length)),
                clipboard_check_interval_ms=int(
                    data.get("check_interval", cls.clipboard_check_interval_ms)
                ),
            )
        except Exception:
            # If file is corrupted, fall back to defaults (don't crash on startup).
            return cls()

    def save(self) -> None:
        path = settings_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        # keep compatibility with old key name
        data["check_interval"] = data.pop("clipboard_check_interval_ms")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def settings_dir() -> Path:
    return Path(user_cache_dir(APP_NAME))


def settings_file() -> Path:
    return settings_dir() / "settings.json"
