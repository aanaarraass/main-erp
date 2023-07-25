from __future__ import print_function
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os.path
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


def auth(client_id, client_secret):
    api_dict = {
        "installed": {
            "client_id": client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": client_secret
        }
    }
    dir_path = os.path.dirname(os.path.realpath(__file__))
    creds = None
    if os.path.exists('{}/googlemeet.token'.format(dir_path)):
        with open('{}/googlemeet.token'.format(dir_path), 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                api_dict, SCOPES)
            creds = flow.run_local_server(port=0)

        with open('{}/googlemeet.token'.format(dir_path), 'wb') as token:
            pickle.dump(creds, token)

    global service
    service = build('calendar', 'v3', credentials=creds)


def create_meeting(title, description, start_time, end_time, alias_id, attendees):

    meeting_body = {
        'summary': title,
        'description': description,

        "end": {
            "dateTime": end_time
        },

        "start": {
            "dateTime": start_time
        },

        "conferenceData": {
            "createRequest": {
                "conferenceSolutionKey": {
                    "type": "hangoutsMeet"
                },
                "requestId": alias_id
            }
        },

        "attendees": attendees,
    }

    meeting = service.events().insert(
        calendarId='primary',
        conferenceDataVersion=1,
        body=meeting_body,
        sendNotifications=True).execute()

    return meeting.get('hangoutLink')
