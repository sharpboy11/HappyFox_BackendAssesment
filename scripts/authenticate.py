from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    # Using a relative path
    credentials_path = os.path.join("config", "credentials.json")
    token_path = os.path.join("config", "token.json")

    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # Ensure the 'config' directory exists before saving the token
    os.makedirs(os.path.dirname(token_path), exist_ok=True)

    with open(token_path, "w") as token:
        token.write(creds.to_json())

    print("✅ Authentication successful! Token saved to 'config/token.json'.")

if __name__ == "__main__":
    authenticate_gmail()
