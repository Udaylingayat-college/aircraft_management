"""
models/hangar.py

CRUD operations for the Hangar table in Aircraft_Fleet_MS.
"""

from aircraft_management.db.connection import get_connection


def get_all():
    """Return all Hangar records joined with Unit name."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT h.*, u.Unit_name "
            "FROM Hangar h "
            "LEFT JOIN Unit u ON h.Unit_id = u.Unit_id "
            "ORDER BY h.Hangar_id"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(hangar_id):
    """Return a single Hangar record by primary key."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Hangar WHERE Hangar_id = %s", (hangar_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data: dict):
    """Insert a new Hangar record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Hangar (Hangar_id, Unit_id, Hangar_name, Capacity) "
            "VALUES (%s, %s, %s, %s)",
            (
                data["Hangar_id"],
                data.get("Unit_id"),
                data["Hangar_name"],
                data.get("Capacity"),
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update(hangar_id, data: dict):
    """Update an existing Hangar record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Hangar SET Unit_id=%s, Hangar_name=%s, Capacity=%s "
            "WHERE Hangar_id=%s",
            (
                data.get("Unit_id"),
                data["Hangar_name"],
                data.get("Capacity"),
                hangar_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete(hangar_id):
    """Delete a Hangar record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Hangar WHERE Hangar_id = %s", (hangar_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_aircraft_count(hangar_id):
    """Return the number of aircraft currently in a hangar."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM Aircraft WHERE Hangar_id = %s", (hangar_id,)
        )
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()
