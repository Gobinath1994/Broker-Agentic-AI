# Standard library imports
import datetime  # For handling date and time
import pickle    # For saving/loading authentication credentials
import os        # For checking file paths

# Google API libraries
from google.auth.transport.requests import Request              # Used for refreshing tokens
from google_auth_oauthlib.flow import InstalledAppFlow          # For handling OAuth2 login flow
from googleapiclient.discovery import build                     # To build the Google Calendar API service

# Define the Google Calendar API scope - this grants permission to manage calendar events
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def authenticate_calendar():
    """
    Authenticates and returns a Google Calendar service client.

    Loads saved credentials from a pickle file if available,
    otherwise triggers an OAuth2 login flow to generate a new token.

    Returns:
        service: Authenticated Google Calendar service object.
    """
    creds = None

    # Check if we already have a valid saved token
    if os.path.exists('tools/token_calendar.pickle'):
        with open('tools/token_calendar.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are found, perform the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the token if it's expired and we have a refresh token
            creds.refresh(Request())
        else:
            # Start the OAuth flow using client credentials
            flow = InstalledAppFlow.from_client_secrets_file(
                'tools/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the new token for future runs
        with open('tools/token_calendar.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Return the authorized Google Calendar API service client
    return build('calendar', 'v3', credentials=creds)

def schedule_event(event):
    """
    Schedules a calendar event in the user's primary Google Calendar.

    Args:
        event (dict): Dictionary containing:
            - 'title' (str): Title of the event
            - 'time' (str): ISO 8601 formatted start datetime (e.g., "2025-06-10T15:00:00")

    Example:
        schedule_event({"title": "Client Call", "time": "2025-06-10T15:00:00"})
    """
    # Get authenticated calendar service
    service = authenticate_calendar()

    # Get the current UTC time in ISO format with 'Z' suffix
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    # Create event body using Google Calendar API format
    calendar_event = {
        'summary': event['title'],  # Title of the event
        'start': {
            'dateTime': event['time'],  # Start time
            'timeZone': 'UTC',          # Time zone
        },
        'end': {
            # End time is 1 hour after start
            'dateTime': (datetime.datetime.fromisoformat(event['time']) + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        }
    }

    # Insert the event into the primary calendar
    created_event = service.events().insert(calendarId='primary', body=calendar_event).execute()

    # Output the link to view the event in the user's calendar
    print(f"Event created: {created_event.get('htmlLink')}")