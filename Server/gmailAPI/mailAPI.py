import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_creds():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("mail_token.json"):
        creds = Credentials.from_authorized_user_file("mail_token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "mail_credentials.json", SCOPES
            )   
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("mail_token.json", "w") as token:
                token.write(creds.to_json())
    return creds



def get_priority_mails(file_loc,userid='me',ResultNumber=5):
# Call the Gmail API
    service = build("gmail", "v1", credentials=get_creds())
    with open(file_loc, "r", encoding="utf-8") as f:
        email_users = json.load(f)
    email_users = email_users[userid]
    qu = "{"
    for email in email_users:
        qu += f"from:{email} "
    qu += "}"
    results = service.users().messages().list(userId=userid, labelIds=["INBOX"],q = qu,maxResults=ResultNumber).execute()
    messages = results.get("messages", [])
    return messages


def get_mail_content(message_id,userid='me'):
    service = build("gmail", "v1", credentials=get_creds())
    message = service.users().messages().get(userId=userid, id=message_id).execute()
    return message.get("snippet", "")





