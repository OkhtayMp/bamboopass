from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QColorDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..constants import DEFAULT_REPO_URL
from ..storage import Settings
from ..version import get_version


class SettingsWindow(QWidget):
    """A small scrollable settings window."""

    def __init__(self, settings: Settings):
        super().__init__()
        self._settings = settings

        self.setWindowTitle("Settings")
        self.setFixedSize(480, 520)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        warning = QLabel(
            "⚠ IMPORTANT SECURITY NOTICE\n\n"
            "Changing 'Iterations' or 'Password Length' WILL generate different passwords.\n"
            "If modified, previously generated passwords will NOT match.\n\n"
            "• Background Color only affects UI appearance.\n"
            "• Clipboard Interval only affects auto-close behavior."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            """QLabel {
  background-color: #fff3cd;
  border: 2px solid #ffcc00;
  border-radius: 10px;
  padding: 14px;
  font-weight: 600;
  color: #7a5200;
}
"""
        )
        layout.addWidget(warning)

        # Background color row
        row = QHBoxLayout()
        row.addWidget(QLabel("Background Color:"))

        self.color_value = QLabel(self._settings.bg_color)
        self.color_value.setStyleSheet("font-weight: 700;")
        row.addWidget(self.color_value)

        choose = QPushButton("Choose")
        choose.setCursor(QCursor(Qt.PointingHandCursor))
        choose.clicked.connect(self._choose_color)
        row.addWidget(choose)
        layout.addLayout(row)

        # Iterations
        layout.addWidget(QLabel("Iterations ⚠ (Changes Password Output)"))
        self.iter_spin = QSpinBox()
        self.iter_spin.setRange(1_000, 1_000_000)
        self.iter_spin.setValue(self._settings.iterations)
        layout.addWidget(self.iter_spin)

        # Password length
        layout.addWidget(QLabel("Password Length ⚠ (Changes Password Output)"))
        self.len_spin = QSpinBox()
        self.len_spin.setRange(8, 128)
        self.len_spin.setValue(self._settings.password_length)
        layout.addWidget(self.len_spin)

        # Clipboard interval
        layout.addWidget(QLabel("Clipboard Check Interval (ms)"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(10, 5_000)
        self.interval_spin.setValue(self._settings.clipboard_check_interval_ms)
        layout.addWidget(self.interval_spin)

        repo_label = QLabel(f"GitHub Repo: <a href='{DEFAULT_REPO_URL}'>{DEFAULT_REPO_URL}</a>")
        repo_label.setOpenExternalLinks(True)
        repo_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        repo_label.setStyleSheet("font-weight: 700; color: #0066cc;")
        layout.addWidget(repo_label)

        version_label = QLabel(f"App Version: {get_version()}")
        version_label.setStyleSheet("font-weight: 700; color: #2e8b57;")
        layout.addWidget(version_label)

        # Buttons row
        buttons = QHBoxLayout()

        reset_btn = QPushButton("🔄 Reset to Default")
        reset_btn.setCursor(QCursor(Qt.PointingHandCursor))
        reset_btn.clicked.connect(self._reset_defaults)

        save_btn = QPushButton("💾 Save and Close")
        save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        save_btn.clicked.connect(self._save_and_close)

        buttons.addWidget(reset_btn)
        buttons.addWidget(save_btn)
        layout.addLayout(buttons)

        layout.addStretch()
        scroll.setWidget(page)
        root.addWidget(scroll)

    def _choose_color(self) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            self._settings.bg_color = color.name()
            self.color_value.setText(self._settings.bg_color)

    def _reset_defaults(self) -> None:
        self._settings = Settings()
        self.color_value.setText(self._settings.bg_color)
        self.iter_spin.setValue(self._settings.iterations)
        self.len_spin.setValue(self._settings.password_length)
        self.interval_spin.setValue(self._settings.clipboard_check_interval_ms)

    def _save_and_close(self) -> None:
        self._settings.bg_color = self.color_value.text()
        self._settings.iterations = int(self.iter_spin.value())
        self._settings.password_length = int(self.len_spin.value())
        self._settings.clipboard_check_interval_ms = int(self.interval_spin.value())
        self._settings.save()
        self.close()

    @property
    def settings(self) -> Settings:
        return self._settings
