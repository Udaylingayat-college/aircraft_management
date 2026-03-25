# Aircraft Fleet Management System

A complete fleet management system with:
- **Legacy Desktop App** — PyQt6 desktop application (original)
- **Web Frontend** — React + TypeScript (Vite) with a FastAPI bridge

---

## Project Structure

```
aircraft_management/
├── main.py                        # PyQt6 desktop entry point
├── api_server.py                  # FastAPI REST bridge (new)
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
├── ui/                            # PyQt6 UI (original desktop app)
└── fleet-frontend/                # React + TypeScript web frontend
    ├── src/
    │   ├── api/client.ts          # Axios API client (base: http://localhost:8000)
    │   ├── components/            # Sidebar, DataTable, FormDialog, StatusBadge, Toast, ProgressBar
    │   ├── pages/                 # Dashboard, Units, Hangars, Aircraft, Assets, Transactions, Inspections
    │   └── styles/global.css      # CSS variables + IBM Plex Sans font
    └── package.json
```

---

## Requirements

- Python 3.10+
- MySQL Server (running locally on `localhost`)
- Node.js 18+ / npm 9+

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
pip install -r requirements.txt
python -m aircraft_management.db.seed
```

### 3. Start the API Server (FastAPI)

```bash
pip install fastapi uvicorn
uvicorn api_server:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### 4. Start the Web Frontend (React)

```bash
cd fleet-frontend
npm install
npm run dev
```

The web app will be available at `http://localhost:5173`.

### 5. (Optional) Run the Legacy Desktop App

```bash
python main.py
```

---

## Web Frontend Features

- **Dashboard** — summary cards (total aircraft, active units, available assets, overdue inspections), recent transactions, upcoming inspections
- **Units** — full CRUD with status badges and filters
- **Hangars** — CRUD with capacity usage progress bars
- **Aircraft** — CRUD with Unit/Status filter dropdowns
- **Assets** — CRUD with color-coded criticality (red = Critical, amber = High)
- **Transactions** — CRUD, still-issued rows highlighted amber
- **Inspections** — CRUD, overdue rows highlighted red, expiring-soon rows amber
- **Real-time search** across every table
- **Toast notifications** auto-hide after 3 seconds

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Web Frontend | React 19 + TypeScript (Vite)        |
| API Bridge   | FastAPI + Uvicorn                   |
| Legacy UI    | PyQt6 (pure Python widgets)         |
| Backend      | Python + mysql-connector-python     |
| Database     | MySQL (`Aircraft_Fleet_MS`)         |
