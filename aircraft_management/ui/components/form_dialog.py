"""
ui/components/form_dialog.py

Generic add/edit form dialog that builds input widgets from a field specification.
Supports QLineEdit, QComboBox, QDateEdit, QSpinBox, and QTextEdit fields.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QDateEdit, QSpinBox,
    QPushButton, QTextEdit, QFrame, QWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QKeySequence, QShortcut

from aircraft_management.ui.styles import FORM_STYLE


class FormDialog(QDialog):
    """
    A reusable modal form dialog.

    Parameters
    ----------
    title : str
        Dialog window title.
    fields : list[dict]
        Each dict defines one field:
        {
            "key": str,                  # Data dict key
            "label": str,                # Human-readable label
            "type": "text"|"combo"|"date"|"spin"|"textarea",
            "required": bool,            # Default False
            "options": list[str],        # For combo only
            "option_ids": list,          # Parallel IDs list for combo (optional)
            "readonly": bool,            # Makes the field read-only
            "placeholder": str,          # Placeholder text
        }
    data : dict | None
        Pre-fill data for edit mode.  Keys match field["key"].
    parent : QWidget | None
    """

    def __init__(self, title: str, fields: list, data: dict = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(460)
        self.setModal(True)
        self.setStyleSheet(FORM_STYLE)

        self._fields = fields
        self._data = data or {}
        self._widgets: dict[str, QWidget] = {}
        self._result_data: dict = {}

        self._build_ui(title)

        # Escape closes the dialog
        QShortcut(QKeySequence("Escape"), self, self.reject)

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self, title: str):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(28, 24, 28, 24)
        outer.setSpacing(16)

        # Title label
        lbl_title = QLabel(title)
        lbl_title.setObjectName("FormTitle")
        outer.addWidget(lbl_title)

        # Thin separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #E2E8F0; max-height: 1px; border: none;")
        outer.addWidget(sep)

        # Form layout
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form.setSpacing(12)
        form.setContentsMargins(0, 8, 0, 8)

        for field in self._fields:
            key = field["key"]
            label_text = field.get("label", key)
            required = field.get("required", False)
            ftype = field.get("type", "text")
            readonly = field.get("readonly", False)

            # Build the label
            lbl = QLabel(f"{label_text}{'  *' if required else ''}")
            lbl.setObjectName("FieldLabel")

            # Build the input widget
            widget = self._make_widget(field)
            self._widgets[key] = widget

            if readonly and hasattr(widget, "setReadOnly"):
                widget.setReadOnly(True)

            form.addRow(lbl, widget)

        outer.addLayout(form)

        # Spacer
        outer.addSpacing(8)

        # Button row
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("CancelBtn")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Save")
        btn_save.setObjectName("SaveBtn")
        btn_save.clicked.connect(self._on_save)
        btn_save.setDefault(True)

        btn_row.addWidget(btn_cancel)
        btn_row.addSpacing(8)
        btn_row.addWidget(btn_save)

        outer.addLayout(btn_row)

    def _make_widget(self, field: dict) -> QWidget:
        """Create and pre-fill the appropriate input widget for a field."""
        key = field["key"]
        ftype = field.get("type", "text")
        value = self._data.get(key)
        placeholder = field.get("placeholder", "")

        if ftype == "combo":
            widget = QComboBox()
            options = field.get("options", [])
            option_ids = field.get("option_ids", options)
            widget.addItems(options)
            widget.setProperty("option_ids", option_ids)
            # Pre-select current value
            if value is not None:
                # Try matching by ID first
                try:
                    idx = list(option_ids).index(value)
                    widget.setCurrentIndex(idx)
                except (ValueError, TypeError):
                    # Try matching by display text
                    idx = widget.findText(str(value))
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
            return widget

        if ftype == "date":
            widget = QDateEdit()
            widget.setCalendarPopup(True)
            widget.setDisplayFormat("yyyy-MM-dd")
            if value:
                if hasattr(value, "year"):
                    widget.setDate(QDate(value.year, value.month, value.day))
                else:
                    widget.setDate(QDate.fromString(str(value), "yyyy-MM-dd"))
            else:
                widget.setDate(QDate.currentDate())
            return widget

        if ftype == "spin":
            widget = QSpinBox()
            widget.setMinimum(field.get("min", 0))
            widget.setMaximum(field.get("max", 99999))
            if value is not None:
                widget.setValue(int(value))
            return widget

        if ftype == "textarea":
            widget = QTextEdit()
            widget.setFixedHeight(80)
            if value:
                widget.setPlainText(str(value))
            if placeholder:
                widget.setPlaceholderText(placeholder)
            return widget

        # Default: text
        widget = QLineEdit()
        if value is not None:
            widget.setText(str(value))
        if placeholder:
            widget.setPlaceholderText(placeholder)
        return widget

    # ------------------------------------------------------------------
    # Save handler
    # ------------------------------------------------------------------
    def _on_save(self):
        """Validate required fields, collect values, and accept the dialog."""
        valid = True
        for field in self._fields:
            key = field["key"]
            required = field.get("required", False)
            widget = self._widgets.get(key)
            if not widget:
                continue
            # Clear previous invalid styling
            if hasattr(widget, "setProperty"):
                widget.setProperty("invalid", False)
                widget.style().unpolish(widget)
                widget.style().polish(widget)

            if required:
                empty = self._is_empty(widget, field)
                if empty:
                    if hasattr(widget, "setProperty"):
                        widget.setProperty("invalid", True)
                        widget.style().unpolish(widget)
                        widget.style().polish(widget)
                    valid = False

        if not valid:
            return

        # Collect values
        for field in self._fields:
            key = field["key"]
            ftype = field.get("type", "text")
            widget = self._widgets.get(key)
            if widget is None:
                continue
            self._result_data[key] = self._get_value(widget, ftype, field)

        self.accept()

    def _is_empty(self, widget: QWidget, field: dict) -> bool:
        ftype = field.get("type", "text")
        if isinstance(widget, QLineEdit):
            return not widget.text().strip()
        if isinstance(widget, QTextEdit):
            return not widget.toPlainText().strip()
        if isinstance(widget, QComboBox):
            return widget.currentIndex() < 0 or not widget.currentText()
        return False

    def _get_value(self, widget: QWidget, ftype: str, field: dict):
        """Extract the current value from a widget."""
        if isinstance(widget, QComboBox):
            idx = widget.currentIndex()
            option_ids = widget.property("option_ids")
            if option_ids and 0 <= idx < len(option_ids):
                return option_ids[idx]
            return widget.currentText()
        if isinstance(widget, QDateEdit):
            # Return as string; model will convert if needed
            return widget.date().toString("yyyy-MM-dd")
        if isinstance(widget, QSpinBox):
            return widget.value()
        if isinstance(widget, QTextEdit):
            return widget.toPlainText().strip() or None
        if isinstance(widget, QLineEdit):
            return widget.text().strip() or None
        return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_data(self) -> dict:
        """Return the collected form data after the dialog is accepted."""
        return self._result_data
