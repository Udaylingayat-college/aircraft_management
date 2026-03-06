"""
main.py

Entry point for the Aircraft Fleet Management System.
Launches the PyQt6 desktop application.
"""

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from aircraft_management.ui.main_window import MainWindow
from aircraft_management.ui.styles import MAIN_STYLE


def main():
    """Initialize and run the application."""
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(MAIN_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
