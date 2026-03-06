"""
ui/transaction_view.py

Asset Transaction management page.
Rows where Return_date is NULL are highlighted with an amber left border.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QMessageBox, QHeaderView, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from aircraft_management.ui.styles import (
    BUTTON_PRIMARY, SEARCH_STYLE, TEXT_PRIMARY,
    BUTTON_DANGER, BUTTON_EDIT, COLOR_WARNING
)
from aircraft_management.ui.components.data_table import DataTable
from aircraft_management.ui.components.form_dialog import FormDialog
import aircraft_management.models.asset_transaction as txn_model
import aircraft_management.models.asset as asset_model
import aircraft_management.models.unit as unit_model


COLUMNS = [
    "Txn ID", "Asset", "Issue Date", "Return Date",
    "Purpose", "State After Return", "Unit", "Actions"
]


def _build_fields(assets, units):
    asset_names = [a["Asset_name"] for a in assets]
    asset_ids = [a["Asset_id"] for a in assets]
    unit_names = [u["Unit_name"] for u in units]
    unit_ids = [u["Unit_id"] for u in units]
    return [
        {"key": "Transaction_id",    "label": "Transaction ID", "type": "spin", "required": True, "min": 1},
        {"key": "Serial_id",         "label": "Asset",          "type": "combo", "required": True,
         "options": asset_names, "option_ids": asset_ids},
        {"key": "Issue_date",        "label": "Issue Date",     "type": "date"},
        {"key": "Return_date",       "label": "Return Date",    "type": "date"},
        {"key": "Purpose",           "label": "Purpose",        "type": "text"},
        {"key": "State_after_return","label": "State After Return", "type": "text"},
        {"key": "Unit_id",           "label": "Unit",           "type": "combo",
         "options": unit_names, "option_ids": unit_ids},
    ]


def _build_edit_fields(assets, units):
    fields = _build_fields(assets, units)
    fields[0]["readonly"] = True
    return fields


class TransactionView(QWidget):
    """Page for managing Asset Transaction records."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        hdr = QHBoxLayout()
        title = QLabel("Asset Transactions")
        title.setStyleSheet(f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};")
        hdr.addWidget(title)
        hdr.addStretch()

        self._search = QLineEdit()
        self._search.setPlaceholderText("🔍  Search transactions…")
        self._search.setStyleSheet(SEARCH_STYLE)
        self._search.textChanged.connect(self._filter)
        hdr.addWidget(self._search)

        btn_add = QPushButton("＋  Add Transaction")
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
            self._rows = txn_model.get_all()
        except Exception as exc:
            QMessageBox.critical(self, "Database Error", str(exc))
            self._rows = []
        self._populate(self._rows)

    def _populate(self, rows):
        self._table.set_row_count(len(rows))
        for r, rec in enumerate(rows):
            return_date = rec.get("Return_date")
            still_issued = return_date is None

            self._table.set_item(r, 0, rec.get("Transaction_id"))
            self._table.set_item(r, 1, rec.get("Asset_name"))
            self._table.set_item(r, 2, str(rec.get("Issue_date", "")))
            self._table.set_item(r, 3, str(return_date) if return_date else "—")
            self._table.set_item(r, 4, rec.get("Purpose"))
            self._table.set_item(r, 5, rec.get("State_after_return"))
            self._table.set_item(r, 6, rec.get("Unit_name"))
            actions = self._make_action_widget(rec)
            self._table.set_widget(r, 7, actions)

            # Highlight still-issued rows
            if still_issued:
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
            assets = asset_model.get_all()
            units = unit_model.get_all()
        except Exception:
            assets, units = [], []
        dlg = FormDialog("Add Transaction", _build_fields(assets, units), parent=self)
        if dlg.exec():
            try:
                txn_model.create(dlg.get_data())
                self.refresh()
                self._toast("Transaction added.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _edit(self, rec):
        try:
            assets = asset_model.get_all()
            units = unit_model.get_all()
        except Exception:
            assets, units = [], []
        dlg = FormDialog("Edit Transaction", _build_edit_fields(assets, units), data=rec, parent=self)
        if dlg.exec():
            try:
                txn_model.update(rec["Transaction_id"], dlg.get_data())
                self.refresh()
                self._toast("Transaction updated.", "success")
            except Exception as exc:
                QMessageBox.critical(self, "Error", str(exc))

    def _delete(self, rec):
        answer = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete transaction #{rec.get('Transaction_id')}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            try:
                txn_model.delete(rec["Transaction_id"])
                self.refresh()
                self._toast("Transaction deleted.", "info")
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
