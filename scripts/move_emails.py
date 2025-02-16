import os
import logging
import pymysql
import sys
from datetime import datetime

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from db_config import DB_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_db():
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"],
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.MySQLError as err:
        logging.error(f"Database connection failed: {err}")
        return None

def determine_subfolder(email):
    sender = email["sender"].lower()
    subject = email["subject"].lower()
    message = email["message"].lower()

    # Rule 1: All conditions
    if "deepthansh" in sender and "funds" in subject and "investor" in message:
        return "myfunds"
    # Rule 1: Any condition
    elif "deepthansh" in sender or "funds" in subject or "investor" in message:
        return "funds"

    # Rule 2: All conditions
    elif "muthu" in sender and "internships" in subject and "bharathi" in message:
        return "myinternships"
    # Rule 2: Any condition
    elif "muthu" in sender or "internships" in subject or "bharathi" in message:
        return "internships"

    # Rule 3: All conditions
    elif "jniranjananehru" in sender and "hackothan" in subject and ("thanks" in message or "participate" in message):
        return "myhackothan"
    # Rule 3: Any condition
    elif "jniranjananehru" in sender or "hackothan" in subject or "thanks" in message or "participate" in message:
        return "hackothan"

    # If none of the conditions are met
    else:
        return "others"

def move_single_email(email_id, main_folder, subfolder, email_data):
    folder_path = os.path.join("emails", main_folder, subfolder)
    os.makedirs(folder_path, exist_ok=True)

    email_file = os.path.join(folder_path, f"email_{email_id}.txt")
    with open(email_file, "w", encoding='utf-8') as file:
        file.write(f"From: {email_data['sender']}\n")
        file.write(f"To: {email_data['recipient']}\n")
        file.write(f"Subject: {email_data['subject']}\n")
        file.write(f"Date: {email_data['received_datetime']}\n")
        file.write(f"Message: {email_data['message']}\n")

    logging.info(f"Moved email ID {email_id} to {folder_path}")

def move_emails():
    conn = connect_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT email_id, sender, recipient, subject, message, received_datetime, is_read 
            FROM emails
        """)
        emails = cursor.fetchall()

        today_folder = datetime.now().strftime("%Y-%m-%d")
        os.makedirs(os.path.join("emails", today_folder), exist_ok=True)

        for email in emails:
            email_id = email["email_id"]
            is_read = email["is_read"]
            main_folder = "Read" if is_read == 1 else "Unread"
            subfolder = determine_subfolder(email)
            move_single_email(email_id, main_folder, subfolder, email)

            # Move emails received today to today's folder
            received_date = email["received_datetime"].strftime("%Y-%m-%d")
            if received_date == today_folder:
                move_single_email(email_id, today_folder, "", email)

        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error in move_emails: {e}")
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    move_emails()