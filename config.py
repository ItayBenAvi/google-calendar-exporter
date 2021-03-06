#
# External - Those needed to be changed according to usage.
#
CALENDAR_NAME = 'itay5330@gmail.com'

# TODO: Add cron job time to pull events.
# Upper/lower bound (exclusive) for an event's start time to filter by.
# (see "https://developers.google.com/calendar/api/v3/reference/events/list")
EVENTS_DAY_TIME_MAX = 10
EVENTS_DAY_TIME_MIN = -5

# Maps between Google's color IDs to description.
COLORS_IDS_MAPPINGS = {
    None: "default",
    '1': "First Example exercise",
    '2': "Second Example exercise",
}

#
# Internal - You probably don't need to touch.
#
TOKEN_PATH = 'token.json'
CLIENT_SECRET_PATH = 'client_secret.json'
EVENT_FIELDS_TO_INCLUDE = ['colorId', 'created', 'updated', 'creator', 'start', 'end']

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
