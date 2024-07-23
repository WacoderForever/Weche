 
import os  
from google.oauth2 import service_account  
from google.auth.transport.requests import Request  
  
creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://mail.google.com/']  
)  
  
def get_authenticated_client():  
    transport = Request()  
    creds.refresh_token = transport.refresh_token  
    return creds  
