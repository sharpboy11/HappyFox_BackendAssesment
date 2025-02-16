from flask import Flask, jsonify, request
import subprocess
import logging
import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

def setup_folder_structure():
    """Create necessary folder structure if it doesn't exist."""
    base_path = "emails"
    folders = ["Read", "Unread"]
    subfolders = ["internships", "course", "club", "linkedin", "today", "others"]
    
    for folder in folders:
        for subfolder in subfolders:
            path = os.path.join(base_path, folder, subfolder)
            os.makedirs(path, exist_ok=True)
    
    logging.info("Folder structure created successfully")

def process_all_emails():
    """Execute the complete email processing workflow."""
    try:
        # Step 1: Setup folder structure
        setup_folder_structure()
        
        # Step 2: Fetch emails
        logging.info("Starting email fetch process...")
        result = subprocess.run(['python', 'scripts/fetch_emails.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Email fetch failed: {result.stderr}")
        
        # Step 3: Process emails
        logging.info("Starting email processing...")
        result = subprocess.run(['python', 'scripts/process_emails.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Email processing failed: {result.stderr}")
        
        # Step 4: Move emails
        logging.info("Starting email movement...")
        result = subprocess.run(['python', 'scripts/move_emails.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Email movement failed: {result.stderr}")
        
        return True, "Email processing completed successfully"
    except Exception as e:
        logging.error(f"Error in email processing workflow: {e}")
        return False, str(e)

@app.route('/')
def home():
    success, message = process_all_emails()
    
    if success:
        return jsonify({
            "status": "success",
            "message": message,
            "endpoints": {
                "fetch_emails": "GET /fetch-emails",
                "process_emails": "GET /process-emails",
                "move_emails": "POST /move-emails"
            }
        })
    else:
        return jsonify({
            "status": "error",
            "message": f"Failed to process emails: {message}"
        }), 500

@app.route('/fetch-emails', methods=['GET'])
def fetch_emails_endpoint():
    try:
        result = subprocess.run(['python', 'scripts/fetch_emails.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Emails fetched successfully"})
        else:
            return jsonify({"status": "error", "message": result.stderr}), 500
    except Exception as e:
        logging.error(f"Error fetching emails: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/process-emails', methods=['GET'])
def process_emails_endpoint():
    try:
        result = subprocess.run(['python', 'scripts/process_emails.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Emails processed successfully"})
        else:
            return jsonify({"status": "error", "message": result.stderr}), 500
    except Exception as e:
        logging.error(f"Error processing emails: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/move-emails', methods=['POST'])
def move_emails_endpoint():
    try:
        result = subprocess.run(['python', 'scripts/move_emails.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Emails moved successfully"})
        else:
            return jsonify({"status": "error", "message": result.stderr}), 500
    except Exception as e:
        logging.error(f"Error moving emails: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)