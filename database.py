import os
import mysql.connector

# ---------------------------------------------------------------
# AIVEN MYSQL DATABASE CONFIGURATION
# ---------------------------------------------------------------

DB_CONFIG = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT", "27965")),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "defaultdb"),

    # Aiven requires SSL
    "ssl_ca": os.path.join(os.path.dirname(__file__), "ca.pem"),
    "ssl_verify_cert": True,
    "ssl_verify_identity": True,
}


def get_db_connection():
    """
    Opens and returns a new connection to the Aiven MySQL database.
    """
    return mysql.connector.connect(**DB_CONFIG)