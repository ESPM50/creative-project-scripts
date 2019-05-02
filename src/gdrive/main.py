import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1soo7vhUM0Dsq_GllLtBoDfIcYDftAz6IEIHgOtkMwok'

dirname = os.path.dirname(__file__)
CREDENTIALS_JSON = os.path.join(dirname, 'credentials.json')
TOKEN_PICKLE = os.path.join(dirname, 'token.pickle')

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(TOKEN_PICKLE):
    with open(TOKEN_PICKLE, 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_JSON, SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open(TOKEN_PICKLE, 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

if __name__ == '__main__':
    # THIS IS JUST FOR TESTING
    result = sheet.values() \
        .update(spreadsheetId=SPREADSHEET_ID,
            range='A2:B3',
            body={
                'values': [[1,2],[3,'=hello']]
            },
            valueInputOption='USER_ENTERED').execute()
    print(result)
