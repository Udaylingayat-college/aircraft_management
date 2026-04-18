"""
db/seed.py

Runnable script that creates all tables (if not exists) in the Aircraft_Fleet_MS
database and inserts sample data.

Usage:
    python -m aircraft_management.db.seed
"""

import mysql.connector
from mysql.connector import Error

# Connection config WITHOUT specifying the database first so we can CREATE it
BASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
}

DATABASE = "Aircraft_Fleet_MS"

CREATE_DATABASE = f"CREATE DATABASE IF NOT EXISTS {DATABASE}"

USE_DATABASE = f"USE {DATABASE}"

CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS Unit (
        Unit_id   INT          PRIMARY KEY,
        Unit_name VARCHAR(100) NOT NULL,
        Status    VARCHAR(50),
        Unit_type VARCHAR(50),
        Location  VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Hangar (
        Hangar_id   INT          PRIMARY KEY,
        Unit_id     INT,
        Hangar_name VARCHAR(100) NOT NULL,
        Capacity    INT,
        FOREIGN KEY (Unit_id) REFERENCES Unit(Unit_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Aircraft (
        Aircraft_id     INT         PRIMARY KEY,
        Registration_no VARCHAR(50) UNIQUE NOT NULL,
        Aircraft_type   VARCHAR(100),
        Unit_id         INT,
        Hangar_id       INT,
        Status          VARCHAR(50),
        FOREIGN KEY (Unit_id)   REFERENCES Unit(Unit_id),
        FOREIGN KEY (Hangar_id) REFERENCES Hangar(Hangar_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Asset (
        Asset_id   INT          PRIMARY KEY,
        Asset_name VARCHAR(100) NOT NULL,
        Category   VARCHAR(100),
        blocked_at VARCHAR(100),
        Status     VARCHAR(50),
        `Condition`  VARCHAR(50),
        Criticality VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Asset_Transaction (
        Transaction_id    INT          PRIMARY KEY,
        Issue_date        DATE,
        Serial_id         INT,
        Return_date       DATE,
        Purpose           VARCHAR(200),
        State_after_return VARCHAR(100),
        Unit_id           INT,
        FOREIGN KEY (Serial_id) REFERENCES Asset(Asset_id),
        FOREIGN KEY (Unit_id)   REFERENCES Unit(Unit_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Inspection_Record (
        Inspection_id   INT          PRIMARY KEY,
        Aircraft_id     INT,
        Inspection_type VARCHAR(100),
        Inspection_date DATE,
        Valid_till      DATE,
        FOREIGN KEY (Aircraft_id) REFERENCES Aircraft(Aircraft_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
      id INT AUTO_INCREMENT PRIMARY KEY,
      full_name VARCHAR(100) NOT NULL,
      email VARCHAR(150) NOT NULL UNIQUE,
      password_hash VARCHAR(255) NOT NULL,
      role ENUM('admin', 'engineer', 'viewer') NOT NULL DEFAULT 'viewer',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,
]

SAMPLE_DATA = [
    (
        "INSERT IGNORE INTO Unit (Unit_id, Unit_name, Status, Unit_type, Location) VALUES "
        "(%s, %s, %s, %s, %s)",
        [
            (1, "Alpha Squadron", "Active", "Fighter", "Delhi"),
            (2, "Bravo Squadron", "Active", "Transport", "Mumbai"),
            (3, "Charlie Squadron", "Inactive", "Training", "Bangalore"),
        ],
    ),
    (
        "INSERT IGNORE INTO Hangar (Hangar_id, Unit_id, Hangar_name, Capacity) VALUES "
        "(%s, %s, %s, %s)",
        [
            (101, 1, "Hangar A1", 10),
            (102, 1, "Hangar A2", 8),
            (201, 2, "Hangar B1", 12),
        ],
    ),
    (
        "INSERT IGNORE INTO Aircraft "
        "(Aircraft_id, Registration_no, Aircraft_type, Unit_id, Hangar_id, Status) VALUES "
        "(%s, %s, %s, %s, %s, %s)",
        [
            (1001, "IND-001", "Sukhoi Su-30", 1, 101, "Operational"),
            (1002, "IND-002", "Sukhoi Su-30", 1, 102, "Under Maintenance"),
            (2001, "IND-101", "C-17 Globemaster", 2, 201, "Operational"),
        ],
    ),
    (
        "INSERT IGNORE INTO Asset "
        "(Asset_id, Asset_name, Category, blocked_at, Status, `Condition`, Criticality) VALUES "
        "(%s, %s, %s, %s, %s, %s, %s)",
        [
            (5001, "Hydraulic Pump", "Mechanical", "Hangar A1", "Available", "Good", "High"),
            (5002, "Navigation System", "Electronics", "Hangar A2", "Issued", "Fair", "Critical"),
            (5003, "Landing Gear Kit", "Mechanical", "Warehouse", "Available", "Excellent", "Medium"),
        ],
    ),
    (
        "INSERT IGNORE INTO Asset_Transaction "
        "(Transaction_id, Issue_date, Serial_id, Return_date, Purpose, State_after_return, Unit_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        [
            (9001, "2026-01-10", 5002, "2026-01-15", "Aircraft Repair", "Functional", 1),
            (9002, "2026-02-01", 5001, None, "Routine Maintenance", None, 1),
        ],
    ),
    (
        "INSERT IGNORE INTO Inspection_Record "
        "(Inspection_id, Aircraft_id, Inspection_type, Inspection_date, Valid_till) VALUES "
        "(%s, %s, %s, %s, %s)",
        [
            (3001, 1001, "Annual Inspection", "2026-01-05", "2027-01-05"),
            (3002, 1002, "Safety Check", "2026-02-01", "2026-08-01"),
            (3003, 2001, "Engine Inspection", "2026-01-20", "2026-07-20"),
        ],
    ),
]


def seed():
    """Create tables and insert sample data into Aircraft_Fleet_MS."""
    try:
        conn = mysql.connector.connect(**BASE_CONFIG)
        cursor = conn.cursor()

        print(f"Creating database '{DATABASE}' if not exists…")
        cursor.execute(CREATE_DATABASE)
        cursor.execute(USE_DATABASE)

        print("Creating tables…")
        for ddl in CREATE_TABLES:
            cursor.execute(ddl)

        print("Inserting sample data…")
        for sql, rows in SAMPLE_DATA:
            for row in rows:
                cursor.execute(sql, row)

        conn.commit()
        print("Seed completed successfully.")

    except Error as exc:
        print(f"Database error: {exc}")
        raise
    finally:
        if "cursor" in dir():
            cursor.close()
        if "conn" in dir() and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    seed()
