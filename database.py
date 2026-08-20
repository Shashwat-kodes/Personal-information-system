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

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="aiven_pool",
            pool_size=3,
            pool_reset_session=True,
            **DB_CONFIG
        )
    return _pool

def get_db_connection():
    return get_pool().get_connection()