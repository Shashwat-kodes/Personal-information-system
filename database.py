import mysql.connector

# ---------------------------------------------------------------
# DATABASE CONFIGURATION
# Update these values to match your local MySQL setup.
# ---------------------------------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "sexysinha12",
    "database": "pis_db"
}


def get_db_connection():
    """
    Opens and returns a new connection to the MySQL database.
    Each route calls this, uses it, then closes it —
    keeps things simple and avoids stale/shared connections.
    """
    return mysql.connector.connect(**DB_CONFIG)