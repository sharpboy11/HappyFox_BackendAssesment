import pymysql
import logging
from config.db_config import DB_CONFIG

def connect_db():
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
        return conn
    except pymysql.MySQLError as err:
        logging.error(f"Database connection error: {err}")
        return None

def fetch_emails_from_db():
    """Fetch emails from the database."""
    conn = connect_db()
    if conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM emails")
            emails = cursor.fetchall()
        conn.close()
        return emails
    return []
