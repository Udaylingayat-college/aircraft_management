"""
ui/hangar_view.py

Hangar management page — list, add, edit, and delete Hangar records.
Shows capacity usage indicator per hangar.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QHeaderView, QProgressBar
)
from PyQt6.QtCore import Qt

from aircraft_management.ui.styles import (
    BUTTON_PRIMARY, SEARCH_STYLE, TEXT_PRIMARY,
    BUTTON_DANGER, BUTTON_EDIT, ACCENT_PRIMARY
)
from aircraft_management.ui.components.data_table import DataTable
from aircraft_management.ui.components.form_dialog import FormDialog
import aircraft_management.models.hangar as hangar_model
import aircraft_management.models.unit as unit_model


COLUMNS = ["Hangar ID", "Name", "Unit", "Capacity", "Usage", "Actions"]


def _build_fields(units):
    unit_names = [u["Unit_name"] for u in units]
    unit_ids = [u["Unit_id"] for u in units]
    return [
        {"key": "Hangar_id",   "label": "Hangar ID", "type": "spin", "required": True, "min": 1},
        {"key": "Unit_id",     "label": "Unit",       "type": "combo", "required": True,
         "options": unit_names, "option_ids": unit_ids},
        {"key": "Hangar_name", "label": "Name",       "type": "text",  "required": True},
        {"key": "Capacity",    "label": "Capacity",   "type": "spin",  "min": 0, "max": 9999},
    ]


def _build_edit_fields(units):
    fields = _build_fields(units)
    fields[0]["readonly"] = True
    return fields


class HangarView(QWidget):
    """Page for managing Hangar records."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Hangars")
        title.setStyleSheet(f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};")
        hdr.addWidget(title)
        hdr.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Search hangars…")
        self._search.setStyleSheet(SEARCH_STYLE)
        self._search.textChanged.connect(self._filter)
        hdr.addWidget(self._search)

        btn_add = QPushButton("＋  Add Hangar")
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
            self._rows = hangar_model.get_all()
        except Exception as exc:
            QMessageBox.critical(self, "Database Error", str(exc))
            self._rows = []
        self._populate(self._rows)

    def _populate(self, rows):
        self._table.set_row_count(len(rows))
        for r, rec in enumerate(rows):
            self._table.set_item(r, 0, rec.get("Hangar_id"))
            self._table.set_item(r, 1, rec.get("Hangar_name"))
            self._table.set_item(r, 2, rec.get("Unit_name"))
            capacity = rec.get("Capacity") or 0
            self._table.set_item(r, 3, capacity)

            # Capacity usage
            try:
                used = hangar_model.get_aircraft_count(rec["Hangar_id"])
            except Exception:
                used = 0
            usage_w = self._make_usage_widget(used, capacity)
            self._table.set_widget(r, 4, usage_w)

            actions = self._make_action_widget(rec)
            self._table.set_widget(r, 5, actions)
        self._table.resize_columns()

    def _make_usage_widget(self, used: int, capacity: int) -> QWidget:
        w = QWidget()
        hl = QHBoxLayout(w)
        hl.setContentsMargins(6, 4, 6, 4)
        hl.setSpacing(8)

        lbl = QLabel(f"{used}/{capacity}")
        lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 9pt;")
        hl.addWidget(lbl)

        if capacity > 0:
            bar = QProgressBar()
            bar.setRange(0, capacity)
            bar.setValue(min(used, capacity))
            bar.setFixedHeight(10)
            bar.setStyleSheet(
                f"QProgressBar {{ border-radius: 5px; background-color: #E2E8F0; border: none; }}"
                f"QProgressBar::chunk {{ background-color: {ACCENT_PRIMARY}; border-radius: 5px; }}"
            )
            bar.setTextVisible(False)
            hl.addWidget(bar, 1)
        return w

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
        except Exception:
            units = []
        dlg = FormDialog("Add Hangar", _build_fields(units), parent=self)
        if dlg.exec():
            try:
                hangar_model.create(dlg.get_data())
                self.refresh()
                self._toast("Hangar added successfully.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _edit(self, rec):
        try:
            units = unit_model.get_all()
        except Exception:
            units = []
        dlg = FormDialog("Edit Hangar", _build_edit_fields(units), data=rec, parent=self)
        if dlg.exec():
            try:
                hangar_model.update(rec["Hangar_id"], dlg.get_data())
                self.refresh()
                self._toast("Hangar updated.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _delete(self, rec):
        answer = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete hangar '{rec.get('Hangar_name')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                hangar_model.delete(rec["Hangar_id"])
                self.refresh()
                self._toast("Hangar deleted.", "info")
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
