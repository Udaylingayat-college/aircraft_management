"""
ui/aircraft_view.py

Aircraft management page with Unit/Status filter dropdowns.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt

from aircraft_management.ui.styles import (
    BUTTON_PRIMARY, SEARCH_STYLE, TEXT_PRIMARY,
    BUTTON_DANGER, BUTTON_EDIT, TEXT_SECONDARY
)
from aircraft_management.ui.components.data_table import DataTable
from aircraft_management.ui.components.form_dialog import FormDialog
from aircraft_management.ui.components.status_badge import StatusBadge
import aircraft_management.models.aircraft as aircraft_model
import aircraft_management.models.unit as unit_model
import aircraft_management.models.hangar as hangar_model


COLUMNS = ["AC ID", "Registration", "Type", "Unit", "Hangar", "Status", "Actions"]

STATUS_OPTIONS = ["", "Operational", "Under Maintenance", "Grounded", "Decommissioned"]


def _build_fields(units, hangars):
    unit_names = [""] + [u["Unit_name"] for u in units]
    unit_ids = [None] + [u["Unit_id"] for u in units]
    hangar_names = [""] + [h["Hangar_name"] for h in hangars]
    hangar_ids = [None] + [h["Hangar_id"] for h in hangars]
    return [
        {"key": "Aircraft_id",     "label": "Aircraft ID",    "type": "spin",  "required": True, "min": 1},
        {"key": "Registration_no", "label": "Registration No","type": "text",  "required": True},
        {"key": "Aircraft_type",   "label": "Aircraft Type",  "type": "text"},
        {"key": "Unit_id",         "label": "Unit",           "type": "combo",
         "options": unit_names, "option_ids": unit_ids},
        {"key": "Hangar_id",       "label": "Hangar",         "type": "combo",
         "options": hangar_names, "option_ids": hangar_ids},
        {"key": "Status",          "label": "Status",         "type": "combo",
         "options": STATUS_OPTIONS},
    ]


def _build_edit_fields(units, hangars):
    fields = _build_fields(units, hangars)
    fields[0]["readonly"] = True
    return fields


class AircraftView(QWidget):
    """Page for managing Aircraft records."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_rows = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        # Header row
        hdr = QHBoxLayout()
        title = QLabel("Aircraft")
        title.setStyleSheet(f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};")
        hdr.addWidget(title)
        hdr.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Search…")
        self._search.setStyleSheet(SEARCH_STYLE)
        self._search.textChanged.connect(self._apply_filters)
        hdr.addWidget(self._search)

        # Unit filter
        self._unit_filter = QComboBox()
        self._unit_filter.setMinimumWidth(140)
        self._unit_filter.setStyleSheet(
            "QComboBox { background: white; border: 1.5px solid #E2E8F0;"
            " border-radius: 8px; padding: 7px 10px; font-size: 10pt; }"
        )
        self._unit_filter.currentIndexChanged.connect(self._apply_filters)
        hdr.addWidget(self._unit_filter)

        # Status filter
        self._status_filter = QComboBox()
        self._status_filter.setMinimumWidth(160)
        self._status_filter.addItems(["All Status"] + STATUS_OPTIONS[1:])
        self._status_filter.setStyleSheet(
            "QComboBox { background: white; border: 1.5px solid #E2E8F0;"
            " border-radius: 8px; padding: 7px 10px; font-size: 10pt; }"
        )
        self._status_filter.currentIndexChanged.connect(self._apply_filters)
        hdr.addWidget(self._status_filter)

        btn_add = QPushButton("＋  Add Aircraft")
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
            self._all_rows = aircraft_model.get_all()
        except Exception as exc:
            QMessageBox.critical(self, "Database Error", str(exc))
            self._all_rows = []

        # Refresh unit filter
        try:
            self._units = unit_model.get_all()
        except Exception:
            self._units = []

        self._unit_filter.blockSignals(True)
        self._unit_filter.clear()
        self._unit_filter.addItem("All Units")
        for u in self._units:
            self._unit_filter.addItem(u["Unit_name"])
        self._unit_filter.blockSignals(False)

        self._apply_filters()

    def _apply_filters(self):
        text = self._search.text().lower()
        unit_idx = self._unit_filter.currentIndex()
        status_idx = self._status_filter.currentIndex()
        unit_name = self._unit_filter.currentText() if unit_idx > 0 else None
        status = self._status_filter.currentText() if status_idx > 0 else None

        filtered = []
        for rec in self._all_rows:
            if unit_name and rec.get("Unit_name") != unit_name:
                continue
            if status and rec.get("Status") != status:
                continue
            if text:
                combined = " ".join(str(v) for v in rec.values() if v).lower()
                if text not in combined:
                    continue
            filtered.append(rec)

        self._populate(filtered)

    def _populate(self, rows):
        self._table.set_row_count(len(rows))
        for r, rec in enumerate(rows):
            self._table.set_item(r, 0, rec.get("Aircraft_id"))
            self._table.set_item(r, 1, rec.get("Registration_no"))
            self._table.set_item(r, 2, rec.get("Aircraft_type"))
            self._table.set_item(r, 3, rec.get("Unit_name"))
            self._table.set_item(r, 4, rec.get("Hangar_name"))
            badge = StatusBadge(rec.get("Status", ""))
            self._table.set_widget(r, 5, badge)
            actions = self._make_action_widget(rec)
            self._table.set_widget(r, 6, actions)
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
        try:
            units = unit_model.get_all()
            hangars = hangar_model.get_all()
        except Exception:
            units, hangars = [], []
        dlg = FormDialog("Add Aircraft", _build_fields(units, hangars), parent=self)
        if dlg.exec():
            try:
                aircraft_model.create(dlg.get_data())
                self.refresh()
                self._toast("Aircraft added.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _edit(self, rec):
        try:
            units = unit_model.get_all()
            hangars = hangar_model.get_all()
        except Exception:
            units, hangars = [], []
        dlg = FormDialog("Edit Aircraft", _build_edit_fields(units, hangars), data=rec, parent=self)
        if dlg.exec():
            try:
                aircraft_model.update(rec["Aircraft_id"], dlg.get_data())
                self.refresh()
                self._toast("Aircraft updated.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _delete(self, rec):
        answer = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete aircraft '{rec.get('Registration_no')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                aircraft_model.delete(rec["Aircraft_id"])
                self.refresh()
                self._toast("Aircraft deleted.", "info")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _filter(self, text: str):
        self._apply_filters()

    def focus_search(self):
        self._search.setFocus()

    def _toast(self, msg, kind="info"):
        mw = self.window()
        if hasattr(mw, "show_toast"):
            mw.show_toast(msg, kind)
