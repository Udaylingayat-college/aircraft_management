"""
ui/unit_view.py

Unit management page — list, add, edit, and delete Unit records.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut

from aircraft_management.ui.styles import (
    BUTTON_PRIMARY, SEARCH_STYLE, TEXT_PRIMARY, TEXT_SECONDARY,
    BUTTON_DANGER, BUTTON_EDIT
)
from aircraft_management.ui.components.data_table import DataTable
from aircraft_management.ui.components.form_dialog import FormDialog
from aircraft_management.ui.components.status_badge import StatusBadge
import aircraft_management.models.unit as unit_model


COLUMNS = ["Unit ID", "Name", "Status", "Type", "Location", "Actions"]

FIELDS = [
    {"key": "Unit_id",   "label": "Unit ID",   "type": "spin",  "required": True, "min": 1},
    {"key": "Unit_name", "label": "Name",       "type": "text",  "required": True},
    {"key": "Status",    "label": "Status",     "type": "combo", "required": False,
     "options": ["Active", "Inactive", ""]},
    {"key": "Unit_type", "label": "Unit Type",  "type": "text"},
    {"key": "Location",  "label": "Location",   "type": "text"},
]

EDIT_FIELDS = [
    {"key": "Unit_id",   "label": "Unit ID",   "type": "spin",  "required": True,
     "readonly": True, "min": 1},
    {"key": "Unit_name", "label": "Name",       "type": "text",  "required": True},
    {"key": "Status",    "label": "Status",     "type": "combo",
     "options": ["Active", "Inactive", ""]},
    {"key": "Unit_type", "label": "Unit Type",  "type": "text"},
    {"key": "Location",  "label": "Location",   "type": "text"},
]


class UnitView(QWidget):
    """Page for managing Unit records."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    # ------------------------------------------------------------------
    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Header row
        hdr = QHBoxLayout()
        title = QLabel("Units")
        title.setStyleSheet(f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};")
        hdr.addWidget(title)
        hdr.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Search units…")
        self._search.setStyleSheet(SEARCH_STYLE)
        self._search.textChanged.connect(self._filter)
        hdr.addWidget(self._search)

        btn_add = QPushButton("＋  Add Unit")
        btn_add.setStyleSheet(BUTTON_PRIMARY)
        btn_add.clicked.connect(self.open_add_dialog)
        hdr.addWidget(btn_add)

        layout.addLayout(hdr)

        # Table
        self._table = DataTable(COLUMNS)
        self._table.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self._table)

    # ------------------------------------------------------------------
    def refresh(self):
        try:
            self._rows = unit_model.get_all()
        except Exception as exc:
            QMessageBox.critical(self, "Database Error", str(exc))
            self._rows = []
        self._populate(self._rows)

    def _populate(self, rows):
        self._table.set_row_count(len(rows))
        for r, rec in enumerate(rows):
            self._table.set_item(r, 0, rec.get("Unit_id"))
            self._table.set_item(r, 1, rec.get("Unit_name"))
            # Status badge
            badge = StatusBadge(rec.get("Status", ""))
            self._table.set_widget(r, 2, badge)
            self._table.set_item(r, 3, rec.get("Unit_type"))
            self._table.set_item(r, 4, rec.get("Location"))
            # Action buttons
            actions = self._make_action_widget(rec)
            self._table.set_widget(r, 5, actions)
        self._table.resize_columns()

    def _make_action_widget(self, rec):
        w = QWidget()
        hl = QHBoxLayout(w)
        hl.setContentsMargins(6, 2, 6, 2)
        hl.setSpacing(6)

        btn_edit = QPushButton("✏ Edit")
        btn_edit.setStyleSheet(BUTTON_EDIT)
        btn_edit.clicked.connect(lambda _, r=rec: self._edit(r))

        btn_del = QPushButton("🗑 Delete")
        btn_del.setStyleSheet(BUTTON_DANGER)
        btn_del.clicked.connect(lambda _, r=rec: self._delete(r))

        hl.addWidget(btn_edit)
        hl.addWidget(btn_del)
        hl.addStretch()
        return w

    # ------------------------------------------------------------------
    def open_add_dialog(self):
        dlg = FormDialog("Add Unit", FIELDS, parent=self)
        if dlg.exec():
            try:
                unit_model.create(dlg.get_data())
                self.refresh()
                self._toast("Unit added successfully.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _edit(self, rec):
        dlg = FormDialog("Edit Unit", EDIT_FIELDS, data=rec, parent=self)
        if dlg.exec():
            try:
                unit_model.update(rec["Unit_id"], dlg.get_data())
                self.refresh()
                self._toast("Unit updated.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _delete(self, rec):
        answer = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete unit '{rec.get('Unit_name')}'?  This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                unit_model.delete(rec["Unit_id"])
                self.refresh()
                self._toast("Unit deleted.", "info")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    # ------------------------------------------------------------------
    def _filter(self, text: str):
        self._table.filter_rows(text)

    def focus_search(self):
        self._search.setFocus()

    def _toast(self, msg, kind="info"):
        mw = self.window()
        if hasattr(mw, "show_toast"):
            mw.show_toast(msg, kind)
