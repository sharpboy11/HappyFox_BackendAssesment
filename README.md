To run the project, first, clone the repository and navigate to the project folder.
Optionally, create a virtual environment and install the required dependencies using pip install -r requirements.txt.
Next, set up the Gmail API by enabling it on Google Cloud Console, configuring OAuth credentials, and downloading the credentials.json file into the project directory.
Then, set up the MySQL database by starting the MySQL server, creating a database (email_db), and running setup_database.py to initialize the necessary tables.
After that, authenticate and fetch emails by executing fetch_emails.py, which will open a browser for Gmail API authentication. 
Once emails are stored in the database, define rules in rules.json and process them using process_emails.py to apply actions such as marking emails as read/unread or moving them. 
If authentication issues arise, delete token.json and retry authentication. 
Ensure MySQL is running correctly and that all dependencies are installed.
