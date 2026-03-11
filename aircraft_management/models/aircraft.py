"""
models/aircraft.py

CRUD operations for the Aircraft table in Aircraft_Fleet_MS.
"""

from aircraft_management.db.connection import get_connection


def get_all():
    """Return all Aircraft records joined with Unit name and Hangar name."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT a.*, u.Unit_name, h.Hangar_name "
            "FROM Aircraft a "
            "LEFT JOIN Unit u ON a.Unit_id = u.Unit_id "
            "LEFT JOIN Hangar h ON a.Hangar_id = h.Hangar_id "
            "ORDER BY a.Aircraft_id"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(aircraft_id):
    """Return a single Aircraft record by primary key."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Aircraft WHERE Aircraft_id = %s", (aircraft_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data: dict):
    """Insert a new Aircraft record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Aircraft "
            "(Aircraft_id, Registration_no, Aircraft_type, Unit_id, Hangar_id, Status) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                data["Aircraft_id"],
                data["Registration_no"],
                data.get("Aircraft_type"),
                data.get("Unit_id"),
                data.get("Hangar_id"),
                data.get("Status"),
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update(aircraft_id, data: dict):
    """Update an existing Aircraft record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Aircraft SET Registration_no=%s, Aircraft_type=%s, "
            "Unit_id=%s, Hangar_id=%s, Status=%s WHERE Aircraft_id=%s",
            (
                data["Registration_no"],
                data.get("Aircraft_type"),
                data.get("Unit_id"),
                data.get("Hangar_id"),
                data.get("Status"),
                aircraft_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete(aircraft_id):
    """Delete an Aircraft record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Aircraft WHERE Aircraft_id = %s", (aircraft_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_total_count():
    """Return the total number of aircraft."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Aircraft")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def get_aircraft_by_unit(unit_id):
    """Return all aircraft belonging to a specific unit."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT a.*, h.Hangar_name FROM Aircraft a "
            "LEFT JOIN Hangar h ON a.Hangar_id = h.Hangar_id "
            "WHERE a.Unit_id = %s ORDER BY a.Aircraft_id",
            (unit_id,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
