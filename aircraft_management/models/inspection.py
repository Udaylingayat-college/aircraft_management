"""
models/inspection.py

CRUD operations for the Inspection_Record table in Aircraft_Fleet_MS.
"""

from datetime import date

from aircraft_management.db.connection import get_connection


def get_all():
    """Return all Inspection_Record rows joined with Aircraft registration."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT ir.*, a.Registration_no "
            "FROM Inspection_Record ir "
            "LEFT JOIN Aircraft a ON ir.Aircraft_id = a.Aircraft_id "
            "ORDER BY ir.Inspection_date DESC"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(inspection_id):
    """Return a single Inspection_Record by primary key."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Inspection_Record WHERE Inspection_id = %s",
            (inspection_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data: dict):
    """Insert a new Inspection_Record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Inspection_Record "
            "(Inspection_id, Aircraft_id, Inspection_type, Inspection_date, Valid_till) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                data["Inspection_id"],
                data.get("Aircraft_id"),
                data.get("Inspection_type"),
                data.get("Inspection_date"),
                data.get("Valid_till"),
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update(inspection_id, data: dict):
    """Update an existing Inspection_Record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Inspection_Record SET Aircraft_id=%s, Inspection_type=%s, "
            "Inspection_date=%s, Valid_till=%s WHERE Inspection_id=%s",
            (
                data.get("Aircraft_id"),
                data.get("Inspection_type"),
                data.get("Inspection_date"),
                data.get("Valid_till"),
                inspection_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete(inspection_id):
    """Delete an Inspection_Record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Inspection_Record WHERE Inspection_id = %s",
            (inspection_id,),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_overdue_count():
    """Return the count of inspections where Valid_till < today."""
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().isoformat()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM Inspection_Record WHERE Valid_till < %s", (today,)
        )
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()


def get_upcoming(days=30):
    """Return inspections expiring within the next `days` days."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    today = date.today().isoformat()
    try:
        cursor.execute(
            "SELECT ir.*, a.Registration_no "
            "FROM Inspection_Record ir "
            "LEFT JOIN Aircraft a ON ir.Aircraft_id = a.Aircraft_id "
            "WHERE ir.Valid_till >= %s "
            "AND ir.Valid_till <= DATE_ADD(%s, INTERVAL %s DAY) "
            "ORDER BY ir.Valid_till",
            (today, today, days),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
