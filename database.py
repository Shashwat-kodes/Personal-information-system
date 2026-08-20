import os
import mysql.connector
from mysql.connector import pooling

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT", "27965")),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "defaultdb"),
    "ssl_ca": os.path.join(os.path.dirname(__file__), "ca.pem"),
    "ssl_verify_cert": True,
    "ssl_verify_identity": True,
    "connection_timeout": 30,
}

# Create ONE pool when app starts
connection_pool = pooling.MySQLConnectionPool(
    pool_name="aiven_pool",
    pool_size=5,
    pool_reset_session=True,
    **DB_CONFIG
)

def get_db_connection():
    """Get a connection from the pool — auto-returned when conn.close() is called."""
    return connection_pool.get_connection()