import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.auth import exceptions

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def get_authenticated_client():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    try:
        creds.refresh(Request())
    except exceptions.RefreshError:
        raise Exception("Unable to refresh credentials")
    return creds

def build_service():
    creds = get_authenticated_client()
    service = build('gmail', 'v1', credentials=creds)
    return service
