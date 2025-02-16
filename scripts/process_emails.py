import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import logging
from datetime import datetime
import pymysql
from db_config import DB_CONFIG  # Now this should work

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load rules from JSON file
def load_rules():
    # Use the correct relative path to rules.json
    rules_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "rules.json")
    with open(rules_path, "r") as file:
        rules = json.load(file)
    return rules["rules"]

# Connect to the database
def connect_db():
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor  # Add this line
        )
        return conn
    except pymysql.MySQLError as err:
        logging.error(f"Database connection failed: {err}")
        exit(1)

# Process emails based on rules
def process_emails():
    rules = load_rules()
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch all emails from the database
    cursor.execute("SELECT email_id, sender, recipient, subject, message, received_datetime, is_read FROM emails")
    emails = cursor.fetchall()

    for email in emails:
        email_id = email["email_id"]  # Updated from "id" to "email_id"
        sender = email["sender"]
        subject = email["subject"]
        received_date = email["received_datetime"]
        is_read = email["is_read"]

        # Determine the main folder (Read or Unread)
        main_folder = "Read" if is_read == 1 else "Unread"  # Fix: Check if is_read is 1 or 0

        # Default subfolder is "others"
        subfolder = "others"

        # Apply rules to determine the subfolder
        for rule in rules:
            conditions = rule["conditions"]
            predicate = rule["predicate"]
            actions = rule["actions"]

            # Check if all conditions are met
            if predicate == "All":
                if all(check_condition(email, condition) for condition in conditions):
                    subfolder = actions[0]["folder"]
                    break
            # Check if any condition is met
            elif predicate == "Any":
                if any(check_condition(email, condition) for condition in conditions):
                    subfolder = actions[0]["folder"]
                    break

        # Move the email to the appropriate folder
        move_email(email_id, main_folder, subfolder)

    conn.close()

# Check if a condition is met
def check_condition(email, condition):
    field = condition["field"]
    predicate = condition["predicate"]
    value = condition["value"]

    if field == "From":
        email_value = email["sender"]
    elif field == "Subject":
        email_value = email["subject"]
    elif field == "Received Date":
        email_value = email["received_datetime"].date()
        value = datetime.now().date() if value == "today" else value

    if predicate == "contains":
        return value.lower() in email_value.lower()
    elif predicate == "equals":
        return email_value == value
    elif predicate == "less than":
        return email_value < value
    elif predicate == "greater than":
        return email_value > value

    return False

# Move email to the appropriate folder
def move_email(email_id, main_folder, subfolder):
    # Create the folder structure if it doesn't exist
    folder_path = os.path.join("emails", main_folder, subfolder)
    os.makedirs(folder_path, exist_ok=True)

    # Simulate moving the email by printing the action
    logging.info(f"Moving email ID {email_id} to {folder_path}")

if __name__ == "__main__":
    process_emails()