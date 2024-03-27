import datetime
import random
import os.path
import time
import jira

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]
start_day = datetime.datetime(2024, 1, 29, 9, 0, 0).timestamp()
random.seed(time.time())

def make_event( start, end, name, color ):
  curr_event = {
  'summary': name,
  'description': 'hekaton',
  'colorId': color,
  'start': {
    'dateTime': datetime.datetime.fromtimestamp(start-10800).strftime("%Y-%m-%dT%H:%M:%SZ"),
    'timeZone': "Etc/GMT-4",
    },
  'end': {
    'dateTime': datetime.datetime.fromtimestamp(end-10800).strftime("%Y-%m-%dT%H:%M:%SZ"),
    'timeZone': "Etc/GMT-4",
    },
  }

  return curr_event


def event_gen( blocks ):

  tasks = jira.get_issues()
  times = []
  events = []
  start = start_day
  end = 0
  offset = 0
    
  for task in tasks:
    if(type(task.time_estimate)==int):

      end = start + task.time_estimate

      times.append([start,end, task.summary, 2])

      start = end

  while(len(times)>0 and blocks):

    if(times[0][0]+offset < blocks[0][0]):
      if(times[0][1]+offset <= blocks[0][0]):
        events.append(make_event(times[0][0]+offset, times[0][1]+offset, times[0][2], times[0][3]))
        del times[0]
        continue
      else:
        events.append(make_event(times[0][0]+offset, blocks[0][0], times[0][2], times[0][3]))
        times.insert(1,(times[0][0]+(blocks[0][0]-times[0][0]-offset),times[0][1],times[0][2], times[0][3]))
        del times[0]
        offset += blocks[0][1]-blocks[0][0]
        del blocks[0]
        continue
    elif(times[0][0]+offset >= blocks[0][0] and times[0][0]+offset < blocks[0][1]):
      offset += blocks[0][1]-(times[0][0]+offset)
      del blocks[0]
      continue
    else:
      del blocks[0]
      continue

  for tim in times:
    events.append(make_event(tim[0]+offset, tim[1]+offset, tim[2], tim[3]))

  return events

def delete_calendar():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  caldrly_exists= False
  service = build("calendar", "v3", credentials=creds) 
  page_token = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      if(calendar_list_entry['summary'] == "calendarly"):
        caldrly_id = calendar_list_entry["id"]
        service.calendars().delete(calendarId=caldrly_id).execute()
        break
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break


def make_schedule():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  caldrly_exists= False
  service = build("calendar", "v3", credentials=creds) 
  page_token = None
  while True:
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
      if(calendar_list_entry['summary'] == "calendarly"):
        caldrly_id = calendar_list_entry["id"]
        caldrly_exists = True
        break
    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break

  if(not caldrly_exists):
    print("NOT FOUND  ")
    calendarly = {
    'summary': 'calendarly',
    'timeZone': service.calendars().get(calendarId='primary').execute().get("timeZone","Europe/Warsaw")
    }
    created_calendarly = service.calendars().insert(body=calendarly).execute()
    caldrly_id = created_calendarly["id"]

  try:
    service = build("calendar", "v3", credentials=creds)

    start_of_day = start_day
    block_s = []    

    for i in range(5):
      block_result = (
          service.events()
          .list(
              calendarId='primary',
              timeMin= datetime.datetime.fromtimestamp(start_of_day).strftime("%Y-%m-%dT%H:%M:%SZ"),
              timeMax = datetime.datetime.fromtimestamp(start_of_day + 32400).strftime("%Y-%m-%dT%H:%M:%SZ") ,
              maxResults=2500,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      blocks = block_result.get("items", [])

      prev_end = start_of_day
      for block in blocks:
        start = block["start"].get("dateTime",-1)
        end = block["end"].get("dateTime",-1)
        if(start != -1 and end != -1):
          start_sec = time.mktime((time.strptime(start, "%Y-%m-%dT%H:%M:%S%z")))
          end_sec = time.mktime(time.strptime(end, "%Y-%m-%dT%H:%M:%S%z"))
          
          if((start_sec - prev_end)>=10800):
            amt_breaks = int((start_sec-prev_end)//5400)
            if( ((start_sec-prev_end)%5400) < 3600):
              amt_breaks -= 1
            for i in range(amt_breaks):
              block_s.append((prev_end+5400*(i+1), prev_end+5400*(i+1)+1200))     

          block_s.append((start_sec,end_sec))
          prev_end = end_sec

      start_sec = start_of_day + 28800
      amt_breaks = int((start_sec-prev_end)//5400)
      if( (start_sec-prev_end)%5400 < 3600):
        amt_breaks -= 1
            
      for i in range(amt_breaks):
        block_s.append((prev_end+5400*(i+1), prev_end+5400*(i+1)+1200))

      start_of_day += 86400
      block_s.append((start_of_day - 57600, start_of_day))
      prev_end = start_of_day
      


    for b in block_s:
      print(datetime.datetime.fromtimestamp(b[0]).strftime("%A, %B %d, %Y %I:%M:%S"),"****",datetime.datetime.fromtimestamp(b[1]).strftime("%A, %B %d, %Y %I:%M:%S"))

    events = event_gen(block_s)

    print("--laintime--")

    for event in events:
      print(event)
      insert_event = service.events().insert(calendarId=caldrly_id, body=event).execute()    


  except HttpError as error:
    print(f"An error occurred: {error}")

if __name__ == "__main__":
  make_schedule()