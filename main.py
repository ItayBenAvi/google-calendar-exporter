import os
from pprint import pprint
from typing import Dict, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

from config import CLIENT_SECRET_PATH, TOKEN_PATH, CALENDAR_NAME, EVENT_FIELDS_TO_INCLUDE, SCOPES, COLORS_IDS_MAPPINGS


class CredentialsFileNotFound(Exception):
    def __init__(self, client_secret_path):
        super(CredentialsFileNotFo, self).__init__(f"Credentials file not found ({client_secret_path})")


def get_service() -> Resource:
    """
    Connects to Google's API. Snipped from Google API's samples.
    :return: Resource to interact with.
    """
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise CredentialsFileNotFound(CLIENT_SECRET_PATH)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def get_calendar_id(service: Resource, name: str = CALENDAR_NAME) -> str:
    calendars = service.calendarList().list().execute()
    for calendar in calendars['items']:
        if calendar['summary'] == name:
            return calendar['id']


def get_calendar_events(service: Resource, calendar_id: str) -> List[Dict]:
    stripped_events = []

    events = service.events().list(calendarId=calendar_id).execute()['items']

    for event in events:
        stripped_event = {}
        for key in EVENT_FIELDS_TO_INCLUDE:
            stripped_event[key] = event.pop(key, None)
        stripped_events.append(stripped_event)

    return stripped_events


def remove_events_clutter(events: List[Dict]):
    for event in events:
        event['start'] = event['start'].get('dateTime') or event['start'].get('date')
        event['end'] = event['end'].get('dateTime') or event['end'].get('date')
        event['creator'] = event['creator'].get('displayName') or event['creator'].get('email')
        event['colorId'] = COLORS_IDS_MAPPINGS.get(event['colorId'], "Unknown")


def main():
    service = get_service()
    calendar_id = get_calendar_id(service, name=CALENDAR_NAME)
    print(calendar_id)

    events = get_calendar_events(service, calendar_id)
    remove_events_clutter(events)
    pprint(events)


if __name__ == '__main__':
    main()
