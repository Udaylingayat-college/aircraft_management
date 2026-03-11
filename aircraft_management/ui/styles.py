"""
ui/styles.py

Global QSS stylesheet constants for the Aircraft Fleet Management System.
Apply MAIN_STYLE via app.setStyleSheet() in main.py.
"""

# ---------------------------------------------------------------------------
# Color tokens
# ---------------------------------------------------------------------------
BG_APP = "#F5F7FA"
BG_SIDEBAR = "#1E293B"
ACCENT_ACTIVE = "#3B82F6"
BG_CARD = "#FFFFFF"
ACCENT_PRIMARY = "#3B82F6"
COLOR_SUCCESS = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"
TEXT_PRIMARY = "#1E293B"
TEXT_SECONDARY = "#64748B"
BG_ROW_ALT = "#F8FAFC"

# ---------------------------------------------------------------------------
# Main application stylesheet
# ---------------------------------------------------------------------------
MAIN_STYLE = f"""
QWidget {{
    font-family: "Segoe UI", "SF Pro Display", "Inter", sans-serif;
    font-size: 10pt;
    color: {TEXT_PRIMARY};
    background-color: {BG_APP};
}}

QScrollBar:vertical {{
    background: {BG_APP};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: #CBD5E1;
    border-radius: 4px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {BG_APP};
    height: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: #CBD5E1;
    border-radius: 4px;
    min-width: 20px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QToolTip {{
    background-color: {TEXT_PRIMARY};
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
}}
"""

# ---------------------------------------------------------------------------
# Sidebar stylesheet
# ---------------------------------------------------------------------------
SIDEBAR_STYLE = f"""
QWidget#Sidebar {{
    background-color: {BG_SIDEBAR};
    border-right: 1px solid #2D3F55;
}}

QPushButton#SidebarItem {{
    background-color: transparent;
    color: #94A3B8;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-size: 10pt;
    font-weight: 400;
    border-radius: 0px;
}}
QPushButton#SidebarItem:hover {{
    background-color: #273549;
    color: #E2E8F0;
}}
QPushButton#SidebarItem:checked {{
    background-color: {ACCENT_ACTIVE};
    color: white;
    font-weight: 600;
}}

QLabel#AppTitle {{
    color: white;
    font-size: 13pt;
    font-weight: 700;
    padding: 20px 20px 8px 20px;
}}
QLabel#AppSubtitle {{
    color: #64748B;
    font-size: 8pt;
    padding: 0px 20px 16px 20px;
}}
"""

# ---------------------------------------------------------------------------
# Table stylesheet
# ---------------------------------------------------------------------------
TABLE_STYLE = f"""
QTableWidget {{
    background-color: {BG_CARD};
    alternate-background-color: {BG_ROW_ALT};
    border: none;
    gridline-color: transparent;
    border-radius: 8px;
    outline: none;
    selection-background-color: #EFF6FF;
    selection-color: {TEXT_PRIMARY};
}}
QTableWidget::item {{
    padding: 10px 12px;
    border-bottom: 1px solid #F1F5F9;
    border-right: none;
}}
QTableWidget::item:selected {{
    background-color: #EFF6FF;
    color: {TEXT_PRIMARY};
}}
QHeaderView::section {{
    background-color: {BG_SIDEBAR};
    color: white;
    font-weight: 600;
    padding: 10px 12px;
    border: none;
    border-right: 1px solid #2D3F55;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
QHeaderView::section:last {{
    border-right: none;
}}
"""

# ---------------------------------------------------------------------------
# Dashboard card stylesheet
# ---------------------------------------------------------------------------
CARD_STYLE = f"""
QFrame#DashCard {{
    background-color: {BG_CARD};
    border-radius: 12px;
    border: 1px solid #E2E8F0;
}}
QLabel#CardNumber {{
    font-size: 28pt;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}
QLabel#CardLabel {{
    font-size: 9pt;
    color: {TEXT_SECONDARY};
    font-weight: 500;
}}
"""

# ---------------------------------------------------------------------------
# Primary button style
# ---------------------------------------------------------------------------
BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {ACCENT_PRIMARY};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-size: 10pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #2563EB;
}}
QPushButton:pressed {{
    background-color: #1D4ED8;
}}
QPushButton:disabled {{
    background-color: #93C5FD;
}}
"""

# ---------------------------------------------------------------------------
# Danger (delete) button style
# ---------------------------------------------------------------------------
BUTTON_DANGER = f"""
QPushButton {{
    background-color: {COLOR_DANGER};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 9pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #DC2626;
}}
QPushButton:pressed {{
    background-color: #B91C1C;
}}
"""

# ---------------------------------------------------------------------------
# Edit (secondary) button style
# ---------------------------------------------------------------------------
BUTTON_EDIT = f"""
QPushButton {{
    background-color: #E0E7FF;
    color: #4338CA;
    border: none;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 9pt;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #C7D2FE;
}}
"""

# ---------------------------------------------------------------------------
# Form / dialog style
# ---------------------------------------------------------------------------
FORM_STYLE = f"""
QDialog {{
    background-color: {BG_CARD};
    border-radius: 12px;
}}
QLabel#FormTitle {{
    font-size: 14pt;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    padding-bottom: 4px;
}}
QLabel#FieldLabel {{
    font-size: 9pt;
    color: {TEXT_SECONDARY};
    font-weight: 600;
}}
QLineEdit, QComboBox, QSpinBox, QDateEdit, QTextEdit {{
    background-color: {BG_APP};
    border: 1.5px solid #E2E8F0;
    border-radius: 6px;
    padding: 7px 10px;
    font-size: 10pt;
    color: {TEXT_PRIMARY};
    min-height: 20px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTextEdit:focus {{
    border-color: {ACCENT_PRIMARY};
    background-color: white;
}}
QLineEdit[invalid="true"], QComboBox[invalid="true"] {{
    border-color: {COLOR_DANGER};
    background-color: #FFF5F5;
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background-color: white;
    selection-background-color: #EFF6FF;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
}}
QPushButton#SaveBtn {{
    background-color: {ACCENT_PRIMARY};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 22px;
    font-size: 10pt;
    font-weight: 600;
    min-width: 90px;
}}
QPushButton#SaveBtn:hover {{
    background-color: #2563EB;
}}
QPushButton#CancelBtn {{
    background-color: #F1F5F9;
    color: {TEXT_SECONDARY};
    border: none;
    border-radius: 8px;
    padding: 9px 22px;
    font-size: 10pt;
    font-weight: 600;
    min-width: 90px;
}}
QPushButton#CancelBtn:hover {{
    background-color: #E2E8F0;
}}
"""

# ---------------------------------------------------------------------------
# Badge styles (used by StatusBadge widget)
# ---------------------------------------------------------------------------
BADGE_STYLES = {
    "green": (
        "background-color: #D1FAE5; color: #065F46; border-radius: 10px;"
        " padding: 3px 10px; font-size: 8pt; font-weight: 600;"
    ),
    "amber": (
        "background-color: #FEF3C7; color: #92400E; border-radius: 10px;"
        " padding: 3px 10px; font-size: 8pt; font-weight: 600;"
    ),
    "red": (
        "background-color: #FEE2E2; color: #991B1B; border-radius: 10px;"
        " padding: 3px 10px; font-size: 8pt; font-weight: 600;"
    ),
    "blue": (
        "background-color: #DBEAFE; color: #1E40AF; border-radius: 10px;"
        " padding: 3px 10px; font-size: 8pt; font-weight: 600;"
    ),
    "gray": (
        "background-color: #F1F5F9; color: #475569; border-radius: 10px;"
        " padding: 3px 10px; font-size: 8pt; font-weight: 600;"
    ),
}

# ---------------------------------------------------------------------------
# Search bar style
# ---------------------------------------------------------------------------
SEARCH_STYLE = f"""
QLineEdit {{
    background-color: white;
    border: 1.5px solid #E2E8F0;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 10pt;
    color: {TEXT_PRIMARY};
    min-width: 220px;
}}
QLineEdit:focus {{
    border-color: {ACCENT_PRIMARY};
}}
"""
