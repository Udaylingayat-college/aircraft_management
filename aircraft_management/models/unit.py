"""
models/unit.py

CRUD operations for the Unit table in Aircraft_Fleet_MS.
"""

from aircraft_management.db.connection import get_connection


def get_all():
    """Return all Unit records as a list of dicts."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Unit ORDER BY Unit_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(unit_id):
    """Return a single Unit record by primary key."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Unit WHERE Unit_id = %s", (unit_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data: dict):
    """Insert a new Unit record.  data keys: Unit_id, Unit_name, Status, Unit_type, Location."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Unit (Unit_id, Unit_name, Status, Unit_type, Location) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                data["Unit_id"],
                data["Unit_name"],
                data.get("Status"),
                data.get("Unit_type"),
                data.get("Location"),
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update(unit_id, data: dict):
    """Update an existing Unit record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Unit SET Unit_name=%s, Status=%s, Unit_type=%s, Location=%s "
            "WHERE Unit_id=%s",
            (
                data["Unit_name"],
                data.get("Status"),
                data.get("Unit_type"),
                data.get("Location"),
                unit_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete(unit_id):
    """Delete a Unit record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Unit WHERE Unit_id = %s", (unit_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_active_count():
    """Return the number of Active units."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Unit WHERE Status = 'Active'")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()
