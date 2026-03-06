"""
ui/dashboard.py

Dashboard home page showing summary cards, recent transactions, and
upcoming inspection alerts.
"""

from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView,
    QSizePolicy
)
from PyQt6.QtCore import Qt

from aircraft_management.ui.styles import (
    BG_CARD, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT_PRIMARY,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, TABLE_STYLE
)
import aircraft_management.models.aircraft as aircraft_model
import aircraft_management.models.unit as unit_model
import aircraft_management.models.asset as asset_model
import aircraft_management.models.inspection as inspection_model
import aircraft_management.models.asset_transaction as transaction_model


# ---------------------------------------------------------------------------
# Helper widgets
# ---------------------------------------------------------------------------

class SummaryCard(QFrame):
    """A white card with a colored left border showing a count + label."""

    def __init__(self, label: str, value: str, border_color: str, icon: str, parent=None):
        super().__init__(parent)
        self.setObjectName("DashCard")
        self.setStyleSheet(
            f"QFrame#DashCard {{ background-color: {BG_CARD}; border-radius: 12px;"
            f" border-left: 5px solid {border_color};"
            f" border-top: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0;"
            f" border-bottom: 1px solid #E2E8F0; }}"
        )
        self.setFixedHeight(110)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(4)

        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"font-size: 22pt; color: {border_color};")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)

        num_lbl = QLabel(str(value))
        num_lbl.setObjectName("CardNumber")
        num_lbl.setStyleSheet(
            f"font-size: 26pt; font-weight: 700; color: {TEXT_PRIMARY};"
        )

        lbl_lbl = QLabel(label)
        lbl_lbl.setObjectName("CardLabel")
        lbl_lbl.setStyleSheet(f"font-size: 9pt; color: {TEXT_SECONDARY}; font-weight: 500;")

        layout.addWidget(icon_lbl)
        layout.addWidget(num_lbl)
        layout.addWidget(lbl_lbl)


class SectionTitle(QLabel):
    """Styled section header label."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            f"font-size: 12pt; font-weight: 700; color: {TEXT_PRIMARY};"
            " padding-bottom: 4px;"
        )


# ---------------------------------------------------------------------------
# Dashboard view
# ---------------------------------------------------------------------------

class DashboardView(QWidget):
    """Main dashboard page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        scroll.setWidget(container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(24)

        # Page title
        title = QLabel("Dashboard")
        title.setStyleSheet(
            f"font-size: 18pt; font-weight: 700; color: {TEXT_PRIMARY};"
        )
        layout.addWidget(title)

        # Summary cards row
        self._cards_layout = QHBoxLayout()
        self._cards_layout.setSpacing(16)
        layout.addLayout(self._cards_layout)

        # Placeholder card widgets (refreshed later)
        self._card_aircraft = SummaryCard("Total Aircraft", "–", ACCENT_PRIMARY, "✈️")
        self._card_units = SummaryCard("Active Units", "–", COLOR_SUCCESS, "🏢")
        self._card_assets = SummaryCard("Assets Available", "–", COLOR_WARNING, "📦")
        self._card_overdue = SummaryCard("Overdue Inspections", "–", COLOR_DANGER, "⚠️")

        for card in [self._card_aircraft, self._card_units, self._card_assets, self._card_overdue]:
            self._cards_layout.addWidget(card)

        # Recent activity
        layout.addWidget(SectionTitle("Recent Asset Transactions"))

        self._recent_table = self._make_recent_table()
        layout.addWidget(self._recent_table)

        # Upcoming inspections
        layout.addWidget(SectionTitle("Upcoming Inspection Alerts (Next 30 Days)"))

        self._alerts_container = QVBoxLayout()
        self._alerts_container.setSpacing(8)
        layout.addLayout(self._alerts_container)

        layout.addStretch()

    # ------------------------------------------------------------------
    # Table for recent transactions
    # ------------------------------------------------------------------
    def _make_recent_table(self) -> QTableWidget:
        headers = ["ID", "Asset", "Issue Date", "Return Date", "Purpose", "Unit"]
        tbl = QTableWidget(0, len(headers))
        tbl.setHorizontalHeaderLabels(headers)
        tbl.setStyleSheet(TABLE_STYLE)
        tbl.setAlternatingRowColors(True)
        tbl.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        tbl.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tbl.verticalHeader().setVisible(False)
        tbl.setShowGrid(False)
        tbl.horizontalHeader().setStretchLastSection(True)
        tbl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        tbl.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        tbl.setFixedHeight(220)
        return tbl

    # ------------------------------------------------------------------
    # Refresh / data loading
    # ------------------------------------------------------------------
    def refresh(self):
        """Reload all dashboard data from the database."""
        self._load_cards()
        self._load_recent_transactions()
        self._load_upcoming_inspections()

    def _load_cards(self):
        try:
            total_ac = aircraft_model.get_total_count()
        except Exception:
            total_ac = "–"
        try:
            active_units = unit_model.get_active_count()
        except Exception:
            active_units = "–"
        try:
            available_assets = asset_model.get_available_count()
        except Exception:
            available_assets = "–"
        try:
            overdue = inspection_model.get_overdue_count()
        except Exception:
            overdue = "–"

        self._update_card(self._card_aircraft, str(total_ac))
        self._update_card(self._card_units, str(active_units))
        self._update_card(self._card_assets, str(available_assets))
        self._update_card(self._card_overdue, str(overdue))

    def _update_card(self, card: SummaryCard, value: str):
        # Find the CardNumber label child and update it
        for child in card.children():
            if isinstance(child, QLabel) and child.objectName() == "CardNumber":
                child.setText(value)
                return

    def _load_recent_transactions(self):
        try:
            rows = transaction_model.get_recent(5)
        except Exception:
            rows = []

        self._recent_table.setRowCount(len(rows))
        for r, rec in enumerate(rows):
            vals = [
                str(rec.get("Transaction_id", "")),
                rec.get("Asset_name", ""),
                str(rec.get("Issue_date", "")),
                str(rec.get("Return_date", "") or "—"),
                rec.get("Purpose", ""),
                rec.get("Unit_name", ""),
            ]
            for c, v in enumerate(vals):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self._recent_table.setItem(r, c, item)

    def _load_upcoming_inspections(self):
        # Clear previous alerts
        while self._alerts_container.count():
            item = self._alerts_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            rows = inspection_model.get_upcoming(30)
        except Exception:
            rows = []

        if not rows:
            lbl = QLabel("No upcoming inspections in the next 30 days.")
            lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 9pt;")
            self._alerts_container.addWidget(lbl)
            return

        today = date.today()
        for rec in rows:
            valid_till = rec.get("Valid_till")
            reg = rec.get("Registration_no", str(rec.get("Aircraft_id", "")))
            itype = rec.get("Inspection_type", "")

            days_left = (
                (valid_till - today).days
                if hasattr(valid_till, "day")
                else None
            )

            color = COLOR_WARNING if days_left is not None and days_left <= 7 else ACCENT_PRIMARY
            alert = QFrame()
            alert.setStyleSheet(
                f"background-color: #FFF7ED; border-left: 4px solid {color};"
                " border-radius: 6px;"
            )
            row_layout = QHBoxLayout(alert)
            row_layout.setContentsMargins(14, 10, 14, 10)

            text_lbl = QLabel(
                f"<b>{reg}</b> — {itype} "
                f"<span style='color:{TEXT_SECONDARY};'>expires {valid_till}</span>"
            )
            text_lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; font-size: 9pt;")
            row_layout.addWidget(text_lbl)
            row_layout.addStretch()

            if days_left is not None:
                days_lbl = QLabel(f"{days_left} day(s) left")
                days_lbl.setStyleSheet(f"color: {color}; font-weight: 600; font-size: 9pt;")
                row_layout.addWidget(days_lbl)

            self._alerts_container.addWidget(alert)
