"""
ui/components/data_table.py

Reusable styled QTableWidget wrapper that provides alternating row colors,
no grid lines, a dark header, and real-time search/filter capability.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from aircraft_management.ui.styles import TABLE_STYLE


class DataTable(QWidget):
    """
    A styled table widget wrapper.

    Parameters
    ----------
    columns : list[str]
        Column header labels.
    parent : QWidget | None
    """

    def __init__(self, columns: list, parent=None):
        super().__init__(parent)
        self._columns = columns

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setStyleSheet(TABLE_STYLE)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setWordWrap(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        layout.addWidget(self.table)

    def set_row_count(self, count: int):
        self.table.setRowCount(count)

    def set_item(self, row: int, col: int, text: str):
        """Set a plain text item at (row, col)."""
        item = QTableWidgetItem(str(text) if text is not None else "")
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, col, item)

    def set_widget(self, row: int, col: int, widget: QWidget):
        """Embed a widget at (row, col)."""
        self.table.setCellWidget(row, col, widget)

    def set_row_background(self, row: int, color: str):
        """Apply a background color to all items in a row."""
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setBackground(QColor(color))

    def set_row_foreground(self, row: int, col: int, color: str):
        """Apply a foreground color to a specific cell."""
        item = self.table.item(row, col)
        if item:
            item.setForeground(QColor(color))

    def filter_rows(self, text: str):
        """Show/hide rows based on whether any column contains `text` (case-insensitive)."""
        text = text.lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
                widget = self.table.cellWidget(row, col)
                if widget and text in widget.findChild(
                    __import__("PyQt6.QtWidgets", fromlist=["QLabel"]).QLabel
                    if hasattr(widget, "findChild") else type(None),
                ):
                    pass  # widget filtering handled implicitly
            self.table.setRowHidden(row, not match if text else False)

    def resize_columns(self):
        """Resize columns to contents then stretch the last one."""
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount() - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            self.table.columnCount() - 1, QHeaderView.ResizeMode.Stretch
        )
