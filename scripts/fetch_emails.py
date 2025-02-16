import os
import base64
import json
import pymysql
import logging
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Gmail API and Database credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = r"C:\ProjectFeb\BHARU ASSIGNMENT\BHARU ASSIGNMENT\HappyFox\HappyFox\config\credentials.json"

def authenticate_gmail():
    """Authenticate with Gmail API and return the service."""
    logging.info("Authenticating with Gmail API...")
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)
    logging.info("Authentication successful.")
    return build('gmail', 'v1', credentials=creds)

def connect_db():
    """Establish connection with MySQL database using PyMySQL."""
    logging.info("Connecting to MySQL database...")
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="root123",
            database="email_db",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("Connected to MySQL database successfully.")
        return conn
    except pymysql.MySQLError as err:
        logging.error(f"Database connection failed: {err}")
        exit(1)

def fetch_emails():
    """Fetch the first 10 emails from Gmail and store them in MySQL."""
    logging.info("Fetching emails from Gmail API...")
    service = authenticate_gmail()
    
    try:
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        logging.info(f"Total emails fetched: {len(messages)}")

        if not messages:
            logging.warning("No emails found.")
            return
        
        conn = connect_db()
        cursor = conn.cursor()

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg.get('payload', {}).get('headers', [])

            email_data = {
                "sender": next((h['value'] for h in headers if h['name'] == 'From'), "Unknown"),
                "recipient": next((h['value'] for h in headers if h['name'] == 'To'), "Unknown"),
                "subject": next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject"),
                "received_datetime": datetime.fromtimestamp(int(msg.get('internalDate', 0)) / 1000),
                "is_read": 0  # Default to unread
            }

            # Extract email body (handle both plain text & HTML)
            parts = msg.get('payload', {}).get('parts', [])
            email_body = ""
            for part in parts:
                if part.get('mimeType') == 'text/plain':
                    email_body = base64.urlsafe_b64decode(part.get('body', {}).get('data', '')).decode('utf-8', errors='ignore')
                    break
            email_data["message"] = email_body or "No Content"

            # *Print fetched email before inserting into DB*
            logging.info(f"Fetched Email -> Subject: {email_data['subject']}, "
                         f"From: {email_data['sender']}, To: {email_data['recipient']}, "
                         f"Received Date: {email_data['received_datetime']}\nMessage: {email_data['message'][:200]}...\n")

            # Insert email data into MySQL (ID is auto-incremented)
            cursor.execute("""
                INSERT INTO emails (sender, recipient, subject, message, received_datetime, is_read) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (email_data['sender'], email_data['recipient'],
                  email_data['subject'], email_data['message'], 
                  email_data['received_datetime'], email_data['is_read']))

        conn.commit()
        conn.close()
        logging.info("Emails stored in MySQL database successfully.")

    except Exception as e:
        logging.error(f"Error fetching emails: {e}")

if __name__ == "__main__":
    fetch_emails()