"""
models/asset_transaction.py

CRUD operations for the Asset_Transaction table in Aircraft_Fleet_MS.
"""

from aircraft_management.db.connection import get_connection


def get_all():
    """Return all Asset_Transaction records joined with Asset name and Unit name."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT t.*, a.Asset_name, u.Unit_name "
            "FROM Asset_Transaction t "
            "LEFT JOIN Asset a ON t.Serial_id = a.Asset_id "
            "LEFT JOIN Unit u ON t.Unit_id = u.Unit_id "
            "ORDER BY t.Issue_date DESC"
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(transaction_id):
    """Return a single Asset_Transaction record by primary key."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Asset_Transaction WHERE Transaction_id = %s",
            (transaction_id,),
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data: dict):
    """Insert a new Asset_Transaction record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Asset_Transaction "
            "(Transaction_id, Issue_date, Serial_id, Return_date, Purpose, "
            "State_after_return, Unit_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                data["Transaction_id"],
                data.get("Issue_date"),
                data.get("Serial_id"),
                data.get("Return_date"),
                data.get("Purpose"),
                data.get("State_after_return"),
                data.get("Unit_id"),
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update(transaction_id, data: dict):
    """Update an existing Asset_Transaction record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Asset_Transaction SET Issue_date=%s, Serial_id=%s, "
            "Return_date=%s, Purpose=%s, State_after_return=%s, Unit_id=%s "
            "WHERE Transaction_id=%s",
            (
                data.get("Issue_date"),
                data.get("Serial_id"),
                data.get("Return_date"),
                data.get("Purpose"),
                data.get("State_after_return"),
                data.get("Unit_id"),
                transaction_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete(transaction_id):
    """Delete an Asset_Transaction record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Asset_Transaction WHERE Transaction_id = %s",
            (transaction_id,),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_recent(limit=5):
    """Return the N most recent transactions (by Issue_date DESC)."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT t.*, a.Asset_name, u.Unit_name "
            "FROM Asset_Transaction t "
            "LEFT JOIN Asset a ON t.Serial_id = a.Asset_id "
            "LEFT JOIN Unit u ON t.Unit_id = u.Unit_id "
            "ORDER BY t.Issue_date DESC LIMIT %s",
            (limit,),
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
