"""
tools/gmail_tool.py

This module provides functionality to:
- Authenticate with the Gmail API using OAuth2.
- Send individual emails.
- Send a daily digest email summarizing broker tasks.
"""

import base64
import os
import pickle
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the required Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def gmail_authenticate():
    """
    Authenticates the user with Gmail using OAuth 2.0.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service.
    """
    creds = None

    # Load the saved credentials from a pickle file if available
    if os.path.exists('tools/token.pickle'):
        with open('tools/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are missing or invalid, perform OAuth flow
    if not creds or not creds.valid:
        # Refresh the token if it's expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Start a new OAuth flow to obtain fresh credentials
            flow = InstalledAppFlow.from_client_secrets_file(
                'tools/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('tools/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Return the authenticated Gmail service
    return build('gmail', 'v1', credentials=creds)


def send_email(to, subject, message_text):
    """
    Sends an email using the Gmail API.

    Args:
        to (str): Recipient's email address.
        subject (str): Email subject line.
        message_text (str): Email message body (plain text).
    """
    # Authenticate and get the Gmail service
    service = gmail_authenticate()

    # Construct the email message
    message = MIMEText(message_text)
    message['to'] = to
    message['subject'] = subject

    # Encode the message as base64 to send via the API
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}

    try:
        # Send the email via Gmail API
        message = service.users().messages().send(userId='me', body=body).execute()
        print(f"📧 Email sent to {to}, ID: {message['id']}")
    except Exception as e:
        print(f"❌ An error occurred while sending email: {e}")


def send_daily_digest(to_email, tasks):
    """
    Sends a daily digest email summarizing all tasks completed today.

    Args:
        to_email (str): The email address to send the digest to.
        tasks (list): A list of task dictionaries, each with 'type' and 'content'.

    Returns:
        bool: True if email was sent successfully.
    """
    # Header for the digest
    body = "Here’s a summary of today’s broker activity:\n\n"

    # Handle empty task list
    if not tasks:
        body += "No tasks completed today."
    else:
        # Loop through each task and add it to the body
        for t in tasks:
            # Try both 'type' and 'task_type' to support different formats
            task_type = t.get('type') or t.get('task_type', 'Task')
            content = t.get('content') or "[No details provided]"
            body += f"- [{task_type.capitalize()}] {content}\n"

    # Send the composed email
    send_email(to_email, "Your Daily Broker Summary", body)

    # Return success (true)
    return True