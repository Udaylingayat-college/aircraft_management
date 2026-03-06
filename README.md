# Aircraft Fleet Management System

A complete **desktop application** built with **PyQt6** (frontend) and **Python + MySQL** (backend) for managing aircraft fleets, units, hangars, assets, asset transactions, and inspection records.

---

## Project Structure

```
aircraft_management/
├── main.py                        # Entry point
├── db/
│   ├── connection.py              # MySQL connection helper
│   └── seed.py                    # Create tables & insert sample data
├── models/
│   ├── unit.py
│   ├── hangar.py
│   ├── aircraft.py
│   ├── asset.py
│   ├── asset_transaction.py
│   └── inspection.py
├── ui/
│   ├── main_window.py             # Main window + sidebar navigation
│   ├── dashboard.py               # Dashboard with summary cards
│   ├── unit_view.py
│   ├── hangar_view.py
│   ├── aircraft_view.py
│   ├── asset_view.py
│   ├── transaction_view.py
│   ├── inspection_view.py
│   ├── styles.py                  # Global QSS stylesheets
│   └── components/
│       ├── sidebar.py
│       ├── data_table.py
│       ├── form_dialog.py
│       └── status_badge.py
└── resources/icons/
```

---

## Requirements

- Python 3.10+
- MySQL Server (running locally on `localhost`)
- See `requirements.txt` for Python dependencies

```
pip install -r requirements.txt
```

---

## Setup

### 1. Configure the Database

Edit `aircraft_management/db/connection.py` to match your MySQL credentials:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "Aircraft_Fleet_MS",
}
```

### 2. Create Tables & Seed Data

```bash
python -m aircraft_management.db.seed
```

### 3. Run the Application

```bash
python main.py
```

---

## Features

- **Dashboard** — summary cards (total aircraft, active units, available assets, overdue inspections), recent transaction feed, upcoming inspection alerts
- **Units** — full CRUD with status badges
- **Hangars** — CRUD with capacity usage progress bars
- **Aircraft** — CRUD with Unit/Status filter dropdowns
- **Assets** — CRUD with color-coded criticality
- **Transactions** — CRUD, still-issued rows highlighted amber
- **Inspections** — CRUD, overdue rows highlighted red, expiring-soon rows amber
- **Real-time search** across every table
- **Keyboard shortcuts**: `Ctrl+N` (Add New), `Ctrl+F` (Focus Search), `Escape` (Close dialog)
- **Window geometry** persisted between sessions via QSettings
- **Toast notifications** auto-hide after 3 seconds

---

## Tech Stack

| Layer    | Technology                     |
|----------|-------------------------------|
| Frontend | PyQt6 (pure Python widgets)   |
| Backend  | Python + mysql-connector-python |
| Database | MySQL (`Aircraft_Fleet_MS`)   |
