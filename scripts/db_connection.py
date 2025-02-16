import pymysql
import logging
from config.db_config import DB_CONFIG  # Ensure db_config.py exists

def connect_to_database():
    """Connect to MySQL database."""
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("✅ Connected to MySQL database successfully.")
        return conn
    except pymysql.MySQLError as err:
        logging.error(f"❌ Database connection failed: {err}")
        return None
