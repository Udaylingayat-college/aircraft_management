"""
ui/components/sidebar.py

Reusable sidebar navigation widget with styled buttons for each section.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

from aircraft_management.ui.styles import SIDEBAR_STYLE


class Sidebar(QWidget):
    """Left-side navigation panel that emits page_changed(index) when a nav item is clicked."""

    page_changed = pyqtSignal(int)

    # (label_text, icon_emoji)
    NAV_ITEMS = [
        ("🏠  Dashboard", 0),
        ("🏢  Units", 1),
        ("🏗️  Hangars", 2),
        ("✈️  Aircraft", 3),
        ("📦  Assets", 4),
        ("🔄  Transactions", 5),
        ("🔍  Inspections", 6),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)
        self.setStyleSheet(SIDEBAR_STYLE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App title block
        title = QLabel("✈ AirFleet")
        title.setObjectName("AppTitle")
        subtitle = QLabel("Fleet Management System")
        subtitle.setObjectName("AppSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Separator line
        sep = QLabel()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #2D3F55; margin: 0 20px 12px 20px;")
        layout.addWidget(sep)

        # Navigation buttons
        self._buttons: list[QPushButton] = []
        for label, index in self.NAV_ITEMS:
            btn = QPushButton(label)
            btn.setObjectName("SidebarItem")
            btn.setCheckable(True)
            btn.setFixedHeight(46)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=index: self._on_nav(i))
            layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        # Select first item by default
        self._select(0)

    def _on_nav(self, index: int):
        self._select(index)
        self.page_changed.emit(index)

    def _select(self, index: int):
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == index)

    def select_page(self, index: int):
        """Programmatically select a sidebar item without emitting the signal."""
        self._select(index)
