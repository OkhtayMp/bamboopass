from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .storage import Settings
from .ui.main_window import MainWindow


def run() -> int:
    """Start the GUI application.

    Preferred entrypoints:
      - `python -m bamboopass`
      - `bamboopass` (installed console script)
    """
    app = QApplication(sys.argv)
    settings = Settings.load()
    win = MainWindow(settings)
    win.show()
    return app.exec()


def _run_as_script() -> int:
    """Allow running this file directly (e.g. VSCode 'Run Python File').

    This keeps behavior consistent without requiring users to switch run configs.
    """
    # When executed as a script, relative imports won't work because __package__ is empty.
    # Add project root (the directory that contains the `bamboopass/` package) to sys.path
    # and re-import via the package namespace.
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from bamboopass.app import run as pkg_run  # noqa: WPS433 (runtime import)
    return pkg_run()


if __name__ == "__main__":
    if __package__:
        raise SystemExit(run())
    raise SystemExit(_run_as_script())
