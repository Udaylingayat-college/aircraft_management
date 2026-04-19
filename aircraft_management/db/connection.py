"""
db/connection.py

Provides MySQL database connection for the Aircraft Fleet Management System.
Uses mysql-connector-python and supports graceful reconnection handling.
"""

import mysql.connector
from mysql.connector import Error, pooling

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "7879",
    "database": "Aircraft_Fleet_MS",
}

# Connection pool (optional, created lazily)
_pool = None


def _create_pool():
    """Create a MySQL connection pool."""
    global _pool
    try:
        _pool = pooling.MySQLConnectionPool(
            pool_name="aircraft_pool",
            pool_size=5,
            pool_reset_session=True,
            **DB_CONFIG,
        )
    except Error:
        _pool = None


def get_connection():
    """
    Return a MySQL database connection.

    Tries to use the connection pool first; falls back to a direct connection
    if the pool is unavailable.  Raises mysql.connector.Error on failure.
    """
    global _pool
    if _pool is None:
        _create_pool()

    if _pool is not None:
        try:
            return _pool.get_connection()
        except Error:
            pass  # Fall through to direct connection

    # Direct (non-pooled) fallback connection
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = False
    return conn
