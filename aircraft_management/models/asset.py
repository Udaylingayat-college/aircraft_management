"""
models/asset.py

CRUD operations for the Asset table in Aircraft_Fleet_MS.
"""

from aircraft_management.db.connection import get_connection


def get_all():
    """Return all Asset records as a list of dicts."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Asset ORDER BY Asset_id")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def get_by_id(asset_id):
    """Return a single Asset record by primary key."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Asset WHERE Asset_id = %s", (asset_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def create(data: dict):
    """Insert a new Asset record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Asset "
            "(Asset_id, Asset_name, Category, blocked_at, Status, `Condition`, Criticality) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                data["Asset_id"],
                data["Asset_name"],
                data.get("Category"),
                data.get("blocked_at"),
                data.get("Status"),
                data.get("Condition"),
                data.get("Criticality"),
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def update(asset_id, data: dict):
    """Update an existing Asset record."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Asset SET Asset_name=%s, Category=%s, blocked_at=%s, "
            "Status=%s, `Condition`=%s, Criticality=%s WHERE Asset_id=%s",
            (
                data["Asset_name"],
                data.get("Category"),
                data.get("blocked_at"),
                data.get("Status"),
                data.get("Condition"),
                data.get("Criticality"),
                asset_id,
            ),
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def delete(asset_id):
    """Delete an Asset record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Asset WHERE Asset_id = %s", (asset_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def get_available_count():
    """Return the count of assets with Status='Available'."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM Asset WHERE Status = 'Available'")
        return cursor.fetchone()[0]
    finally:
        cursor.close()
        conn.close()
