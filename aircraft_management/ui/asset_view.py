"""
ui/asset_view.py

Asset management page.  Criticality column uses colored text.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

from aircraft_management.ui.styles import (
    BUTTON_PRIMARY, SEARCH_STYLE, TEXT_PRIMARY,
    BUTTON_DANGER, BUTTON_EDIT, COLOR_DANGER, COLOR_WARNING
)
from aircraft_management.ui.components.data_table import DataTable
from aircraft_management.ui.components.form_dialog import FormDialog
from aircraft_management.ui.components.status_badge import StatusBadge
import aircraft_management.models.asset as asset_model


COLUMNS = ["Asset ID", "Name", "Category", "Location", "Status", "Condition", "Criticality", "Actions"]

CRITICALITY_COLORS = {
    "Critical": COLOR_DANGER,
    "High": COLOR_WARNING,
    "Medium": "#3B82F6",
    "Low": "#10B981",
}

FIELDS = [
    {"key": "Asset_id",    "label": "Asset ID",   "type": "spin",  "required": True, "min": 1},
    {"key": "Asset_name",  "label": "Name",        "type": "text",  "required": True},
    {"key": "Category",    "label": "Category",    "type": "text"},
    {"key": "blocked_at",  "label": "Location",    "type": "text"},
    {"key": "Status",      "label": "Status",      "type": "combo",
     "options": ["Available", "Issued", "Under Maintenance", ""]},
    {"key": "Condition",   "label": "Condition",   "type": "combo",
     "options": ["Excellent", "Good", "Fair", "Poor", ""]},
    {"key": "Criticality", "label": "Criticality", "type": "combo",
     "options": ["Critical", "High", "Medium", "Low", ""]},
]

EDIT_FIELDS = [f.copy() for f in FIELDS]
EDIT_FIELDS[0]["readonly"] = True


class AssetView(QWidget):
    """Page for managing Asset records."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Assets")
        title.setStyleSheet(f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};")
        hdr.addWidget(title)
        hdr.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Search assets…")
        self._search.setStyleSheet(SEARCH_STYLE)
        self._search.textChanged.connect(self._filter)
        hdr.addWidget(self._search)

        btn_add = QPushButton("＋  Add Asset")
        btn_add.setStyleSheet(BUTTON_PRIMARY)
        btn_add.clicked.connect(self.open_add_dialog)
        hdr.addWidget(btn_add)

        layout.addLayout(hdr)

        self._table = DataTable(COLUMNS)
        self._table.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self._table)

    def refresh(self):
        try:
            self._rows = asset_model.get_all()
        except Exception as exc:
            QMessageBox.critical(self, "Database Error", str(exc))
            self._rows = []
        self._populate(self._rows)

    def _populate(self, rows):
        self._table.set_row_count(len(rows))
        for r, rec in enumerate(rows):
            self._table.set_item(r, 0, rec.get("Asset_id"))
            self._table.set_item(r, 1, rec.get("Asset_name"))
            self._table.set_item(r, 2, rec.get("Category"))
            self._table.set_item(r, 3, rec.get("blocked_at"))
            badge = StatusBadge(rec.get("Status", ""))
            self._table.set_widget(r, 4, badge)
            self._table.set_item(r, 5, rec.get("Condition"))
            crit = rec.get("Criticality", "")
            self._table.set_item(r, 6, crit)
            color = CRITICALITY_COLORS.get(crit, TEXT_PRIMARY)
            self._table.set_row_foreground(r, 6, color)
            actions = self._make_action_widget(rec)
            self._table.set_widget(r, 7, actions)
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

    def open_add_dialog(self):
        dlg = FormDialog("Add Asset", FIELDS, parent=self)
        if dlg.exec():
            try:
                asset_model.create(dlg.get_data())
                self.refresh()
                self._toast("Asset added.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _edit(self, rec):
        dlg = FormDialog("Edit Asset", EDIT_FIELDS, data=rec, parent=self)
        if dlg.exec():
            try:
                asset_model.update(rec["Asset_id"], dlg.get_data())
                self.refresh()
                self._toast("Asset updated.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _delete(self, rec):
        answer = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete asset '{rec.get('Asset_name')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                asset_model.delete(rec["Asset_id"])
                self.refresh()
                self._toast("Asset deleted.", "info")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _filter(self, text: str):
        self._table.filter_rows(text)

    def focus_search(self):
        self._search.setFocus()

    def _toast(self, msg, kind="info"):
        mw = self.window()
        if hasattr(mw, "show_toast"):
            mw.show_toast(msg, kind)
