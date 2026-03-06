"""
ui/inspection_view.py

Inspection Record management page.
Overdue rows (Valid_till < today) → red highlight.
Expiring within 30 days → amber highlight.
"""

from datetime import date, timedelta

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from aircraft_management.ui.styles import (
    BUTTON_PRIMARY, SEARCH_STYLE, TEXT_PRIMARY,
    BUTTON_DANGER, BUTTON_EDIT, COLOR_DANGER, COLOR_WARNING
)
from aircraft_management.ui.components.data_table import DataTable
from aircraft_management.ui.components.form_dialog import FormDialog
import aircraft_management.models.inspection as inspection_model
import aircraft_management.models.aircraft as aircraft_model


COLUMNS = [
    "Inspection ID", "Registration", "Type",
    "Inspection Date", "Valid Till", "Actions"
]


def _build_fields(aircrafts):
    reg_list = [a["Registration_no"] for a in aircrafts]
    id_list = [a["Aircraft_id"] for a in aircrafts]
    return [
        {"key": "Inspection_id",   "label": "Inspection ID",   "type": "spin", "required": True, "min": 1},
        {"key": "Aircraft_id",     "label": "Aircraft",        "type": "combo", "required": True,
         "options": reg_list, "option_ids": id_list},
        {"key": "Inspection_type", "label": "Inspection Type", "type": "text"},
        {"key": "Inspection_date", "label": "Inspection Date", "type": "date"},
        {"key": "Valid_till",      "label": "Valid Till",      "type": "date"},
    ]


def _build_edit_fields(aircrafts):
    fields = _build_fields(aircrafts)
    fields[0]["readonly"] = True
    return fields


class InspectionView(QWidget):
    """Page for managing Inspection Record records."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Inspections")
        title.setStyleSheet(f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};")
        hdr.addWidget(title)
        hdr.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Search inspections…")
        self._search.setStyleSheet(SEARCH_STYLE)
        self._search.textChanged.connect(self._filter)
        hdr.addWidget(self._search)

        btn_add = QPushButton("＋  Add Inspection")
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
            self._rows = inspection_model.get_all()
        except Exception as exc:
            QMessageBox.critical(self, "Database Error", str(exc))
            self._rows = []
        self._populate(self._rows)

    def _populate(self, rows):
        today = date.today()
        soon = today + timedelta(days=30)
        self._table.set_row_count(len(rows))

        for r, rec in enumerate(rows):
            valid_till = rec.get("Valid_till")

            self._table.set_item(r, 0, rec.get("Inspection_id"))
            self._table.set_item(r, 1, rec.get("Registration_no"))
            self._table.set_item(r, 2, rec.get("Inspection_type"))
            self._table.set_item(r, 3, str(rec.get("Inspection_date", "")))
            self._table.set_item(r, 4, str(valid_till) if valid_till else "")
            actions = self._make_action_widget(rec)
            self._table.set_widget(r, 5, actions)

            # Row highlighting
            if valid_till:
                if hasattr(valid_till, "year"):
                    vt = valid_till
                else:
                    from datetime import date as _date
                    try:
                        vt = _date.fromisoformat(str(valid_till))
                    except ValueError:
                        vt = None

                if vt:
                    if vt < today:
                        self._table.set_row_background(r, "#FFF5F5")
                    elif vt <= soon:
                        self._table.set_row_background(r, "#FFFBEB")

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
            aircrafts = aircraft_model.get_all()
        except Exception:
            aircrafts = []
        dlg = FormDialog("Add Inspection", _build_fields(aircrafts), parent=self)
        if dlg.exec():
            try:
                inspection_model.create(dlg.get_data())
                self.refresh()
                self._toast("Inspection record added.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _edit(self, rec):
        try:
            aircrafts = aircraft_model.get_all()
        except Exception:
            aircrafts = []
        dlg = FormDialog("Edit Inspection", _build_edit_fields(aircrafts), data=rec, parent=self)
        if dlg.exec():
            try:
                inspection_model.update(rec["Inspection_id"], dlg.get_data())
                self.refresh()
                self._toast("Inspection updated.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _delete(self, rec):
        answer = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete inspection #{rec.get('Inspection_id')}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                inspection_model.delete(rec["Inspection_id"])
                self.refresh()
                self._toast("Inspection deleted.", "info")
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
