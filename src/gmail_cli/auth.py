"""
Gmail API Authentication Module
"""

import os
import json
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.compose'
]


class GmailAuthenticator:
    """Handles Gmail API authentication and service creation"""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Gmail API and create service instance
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Credentials file '{self.credentials_file}' not found!")
                    print("Please download your OAuth2 credentials from Google Cloud Console")
                    print("and save them as 'credentials.json' in the project directory.")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('gmail', 'v1', credentials=creds)
            return True
        except Exception as e:
            print(f"❌ Failed to create Gmail service: {e}")
            return False
    
    def get_service(self):
        """Get the authenticated Gmail service instance"""
        if not self.service:
            if not self.authenticate():
                raise Exception("Failed to authenticate with Gmail API")
        return self.service
    
    def revoke_credentials(self) -> bool:
        """
        Revoke stored credentials
        
        Returns:
            bool: True if revocation successful, False otherwise
        """
        try:
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as token:
                    creds_data = json.load(token)
                    creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
                    creds.revoke(Request())
                
                os.remove(self.token_file)
                print("✅ Credentials revoked successfully")
                return True
        except Exception as e:
            print(f"❌ Failed to revoke credentials: {e}")
            return False
        
        return False
