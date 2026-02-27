from __future__ import annotations

from contextlib import suppress

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QCursor, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QPushButton, QWidget

from ..crypto import derive_password
from ..storage import Settings
from ..utils.colors import best_text_colors
from .icons import eye_svg
from .settings_window import SettingsWindow


class MainWindow(QWidget):
    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings

        self._stage: str = "key"  # "key" -> "seed"
        self._key: str = ""
        self._password: str = ""
        self._done: bool = False

        self._eye_pinned_open: bool = False
        self._alt_pressed: bool = False

        self._previous_clipboard: str = QApplication.clipboard().text()

        self._clipboard_timer = QTimer(self)
        self._settings_win: SettingsWindow | None = None

        self._setup_window()
        self._build_ui()

    def _setup_window(self) -> None:
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(520, 60)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 3)

        colors = best_text_colors(self._settings.bg_color)
        self._text_primary = colors.primary
        self._text_secondary = colors.secondary
        self.setStyleSheet(f"background:{self._settings.bg_color}; color:{self._text_primary};")

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 8, 8)
        layout.setSpacing(8)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter key or /set")
        self.input.setEchoMode(QLineEdit.Password)
        self.input.returnPressed.connect(self._next_step)

        self.input.setStyleSheet(
            f"""QLineEdit {{
  background: {self._settings.bg_color};
  border: none;
  color: {self._text_primary};
  font-weight: 700;
  font-size: 24px;
  padding-left: 8px;
}}
QLineEdit:placeholder {{
  color: {self._text_secondary};
}}
"""
        )
        layout.addWidget(self.input)

        self.eye_btn = QPushButton()
        self.eye_btn.setCheckable(True)
        self.eye_btn.setChecked(False)
        self.eye_btn.clicked.connect(self._toggle_eye_pin)
        self.eye_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.eye_btn.setFixedSize(36, 36)
        self.eye_btn.setStyleSheet("QPushButton{background:transparent;border:none;}")
        layout.addWidget(self.eye_btn)

        self.close_btn = QPushButton("✕")
        self.close_btn.clicked.connect(self.close_app)
        self.close_btn.setFixedSize(44, 44)
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setStyleSheet(
            f"""QPushButton {{
  background: transparent;
  border: none;
  color: {self._text_primary};
  font-size: 38px;
  font-weight: 800;
}}
QPushButton:hover {{ color: red; }}
QPushButton:pressed {{ color: darkred; }}
"""
        )
        layout.addWidget(self.close_btn)

        self._sync_visibility()

    def _toggle_eye_pin(self) -> None:
        self._eye_pinned_open = self.eye_btn.isChecked()
        self._sync_visibility()

    def _is_visible(self) -> bool:
        return self._eye_pinned_open or self._alt_pressed

    def _sync_visibility(self) -> None:
        visible = self._is_visible()
        self.input.setEchoMode(QLineEdit.Normal if visible else QLineEdit.Password)

        svg = eye_svg(visible=visible, color=self._text_primary)
        pixmap = QPixmap()
        pixmap.loadFromData(svg.encode("utf-8"), "SVG")
        self.eye_btn.setIcon(QIcon(pixmap))
        self.eye_btn.setIconSize(pixmap.size())

    def keyPressEvent(self, event):  # noqa: N802 (Qt naming)
        if event.key() == Qt.Key_Alt:
            if not self._alt_pressed:
                self._alt_pressed = True
                self._sync_visibility()
            return
        if event.key() == Qt.Key_Escape:
            self.close_app()
            return
        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):  # noqa: N802 (Qt naming)
        if event.key() == Qt.Key_Alt:
            self._alt_pressed = False
            self._sync_visibility()
            return
        super().keyReleaseEvent(event)

    def _next_step(self) -> None:
        value = self.input.text().strip()
        if not value or self._done:
            return

        if value.lower() == "/set":
            self._settings_win = SettingsWindow(self._settings)
            self._settings_win.show()
            self.close()
            return

        if self._stage == "key":
            self._key = value
            self._stage = "seed"
            self.input.clear()
            self.input.setPlaceholderText("Enter seed (domain/site)...")
            self.input.setEchoMode(QLineEdit.Password)
            self._sync_visibility()
            return

        if self._stage == "seed":
            self._previous_clipboard = QApplication.clipboard().text()

            self._password = derive_password(
                key=self._key,
                seed=value,
                iterations=self._settings.iterations,
                length=self._settings.password_length,
            )
            QApplication.clipboard().setText(self._password)

            self._done = True
            self.hide()

            self._clipboard_timer.timeout.connect(self._check_clipboard)
            self._clipboard_timer.start(self._settings.clipboard_check_interval_ms)

    def _check_clipboard(self) -> None:
        # If user copied something else, close and restore previous clipboard
        if self._done and QApplication.clipboard().text() != self._password:
            self.close_app()

    def close_app(self) -> None:
        with suppress(Exception):
            self._clipboard_timer.stop()

        clipboard = QApplication.clipboard()
        if clipboard.text() == self._password:
            clipboard.setText(self._previous_clipboard)

        self.close()
        QApplication.quit()
        raise SystemExit(0)
