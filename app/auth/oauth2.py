import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.auth import exceptions

# Load the service account key
creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/gmail.send']
)

def get_authenticated_client():
    try:
        creds.refresh(Request())
    except exceptions.RefreshError:
        raise Exception("Unable to refresh credentials")
    return creds
