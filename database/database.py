import mysql.connector
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Define the log format
    handlers=[
        logging.FileHandler("database.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def connect_db():
    """Connect to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="email_db"
        )
        logging.info("Successfully connected to the database.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to the database: {err}")
        raise

def create_table():
    """Create the 'emails' table if it doesn't exist."""
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # SQL query to create the table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id VARCHAR(255) PRIMARY KEY,
                sender VARCHAR(255),
                recipient VARCHAR(255),
                subject TEXT,
                message TEXT,
                received_date DATETIME,
                read_status BOOLEAN DEFAULT FALSE
            )
        """)
        
        conn.commit()
        logging.info("Table 'emails' created or already exists.")
    except mysql.connector.Error as err:
        logging.error(f"Error creating table: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    logging.info("Starting script to create 'emails' table.")
    create_table()
    logging.info("Script execution completed.")