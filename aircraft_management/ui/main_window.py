"""
ui/main_window.py

Main application window for the Aircraft Fleet Management System.
Contains a fixed-width sidebar on the left and a stacked widget on the right.
Window size/position is persisted using QSettings.
"""

import sys

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget,
    QMessageBox, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QSettings, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QKeySequence, QShortcut

from aircraft_management.ui.components.sidebar import Sidebar
from aircraft_management.ui.dashboard import DashboardView
from aircraft_management.ui.unit_view import UnitView
from aircraft_management.ui.hangar_view import HangarView
from aircraft_management.ui.aircraft_view import AircraftView
from aircraft_management.ui.asset_view import AssetView
from aircraft_management.ui.transaction_view import TransactionView
from aircraft_management.ui.inspection_view import InspectionView


class ToastNotification(QLabel):
    """Auto-hiding toast notification displayed at top-right of the window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(42)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            "background-color: #1E293B; color: white; border-radius: 8px;"
            " padding: 8px 18px; font-size: 10pt; font-weight: 500;"
        )
        self.hide()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_message(self, message: str, kind: str = "info"):
        """Display a message for 3 seconds.  kind: 'info', 'success', 'error'."""
        colors = {
            "success": ("#065F46", "#D1FAE5"),
            "error": ("#991B1B", "#FEE2E2"),
            "info": ("#1E293B", "#DBEAFE"),
        }
        text_color, bg_color = colors.get(kind, colors["info"])
        self.setStyleSheet(
            f"background-color: {bg_color}; color: {text_color}; border-radius: 8px;"
            " padding: 8px 18px; font-size: 10pt; font-weight: 500;"
        )
        self.setText(message)
        self.adjustSize()
        self.setMinimumWidth(max(200, self.width()))
        self._reposition()
        self.show()
        self.raise_()
        self._timer.start(3000)

    def _reposition(self):
        if self.parent():
            pw = self.parent().width()
            self.move(pw - self.width() - 20, 60)


class MainWindow(QMainWindow):
    """Application main window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aircraft Fleet Management System")
        self.setMinimumSize(1200, 700)

        self._restore_geometry()
        self._build_ui()
        self._setup_shortcuts()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._switch_page)
        root_layout.addWidget(self.sidebar)

        # Content area
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #F5F7FA;")
        content_layout = QHBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)
        root_layout.addWidget(content_frame, 1)

        # Create views
        self._dashboard = DashboardView(self)
        self._unit_view = UnitView(self)
        self._hangar_view = HangarView(self)
        self._aircraft_view = AircraftView(self)
        self._asset_view = AssetView(self)
        self._transaction_view = TransactionView(self)
        self._inspection_view = InspectionView(self)

        for view in [
            self._dashboard,
            self._unit_view,
            self._hangar_view,
            self._aircraft_view,
            self._asset_view,
            self._transaction_view,
            self._inspection_view,
        ]:
            self.stack.addWidget(view)

        # Toast overlay
        self._toast = ToastNotification(self)

    def _switch_page(self, index: int):
        self.stack.setCurrentIndex(index)
        # Refresh data when switching views
        current = self.stack.currentWidget()
        if hasattr(current, "refresh"):
            current.refresh()

    def _setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+N"), self, self._add_new)
        QShortcut(QKeySequence("Ctrl+F"), self, self._focus_search)
        QShortcut(QKeySequence("Escape"), self, self._escape)

    def _add_new(self):
        current = self.stack.currentWidget()
        if hasattr(current, "open_add_dialog"):
            current.open_add_dialog()

    def _focus_search(self):
        current = self.stack.currentWidget()
        if hasattr(current, "focus_search"):
            current.focus_search()

    def _escape(self):
        # Close any open child dialog
        for child in self.findChildren(QMessageBox):
            child.reject()

    # ------------------------------------------------------------------
    # Toast helper (accessible from child views via parent())
    # ------------------------------------------------------------------
    def show_toast(self, message: str, kind: str = "info"):
        self._toast.show_message(message, kind)

    # ------------------------------------------------------------------
    # Window geometry persistence
    # ------------------------------------------------------------------
    def _restore_geometry(self):
        settings = QSettings("AirFleet", "AircraftMgmt")
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        settings = QSettings("AirFleet", "AircraftMgmt")
        settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._toast._reposition()
