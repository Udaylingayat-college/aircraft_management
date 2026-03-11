"""
ui/components/status_badge.py

A small colored label widget that represents a status value with a color-coded badge.
"""

from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from aircraft_management.ui.styles import BADGE_STYLES

# Map status strings (lowercase) → badge variant key
_STATUS_MAP = {
    # Green variants
    "operational": "green",
    "active": "green",
    "available": "green",
    "functional": "green",
    "excellent": "green",
    # Amber variants
    "under maintenance": "amber",
    "inactive": "amber",
    "issued": "amber",
    "fair": "amber",
    "medium": "blue",
    # Red variants
    "grounded": "red",
    "decommissioned": "red",
    "critical": "red",
    # Blue / gray fallbacks
    "good": "blue",
    "high": "amber",
    "low": "green",
}


def get_badge_variant(status: str) -> str:
    """Return the badge variant ('green', 'amber', 'red', 'blue', 'gray') for a status string."""
    if not status:
        return "gray"
    return _STATUS_MAP.get(status.lower(), "gray")


class StatusBadge(QLabel):
    """A colored pill-shaped label for displaying status values."""

    def __init__(self, status: str, parent=None):
        super().__init__(status or "—", parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        variant = get_badge_variant(status)
        self.setStyleSheet(BADGE_STYLES.get(variant, BADGE_STYLES["gray"]))
