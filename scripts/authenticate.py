from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file("C:\ProjectFeb\BHARU ASSIGNMENT\BHARU ASSIGNMENT\HappyFox\HappyFox\config\credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("config/token.json", "w") as token:
        token.write(creds.to_json())

    print("✅ Authentication successful! Token saved to 'config/token.json'.")

if __name__ == "__main__":
    authenticate_gmail()
