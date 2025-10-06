# import datetime
# from googleapiclient.discovery import build
# import os
# import time as get_time
# from google.oauth2.credentials import Credentials
# from dateutil import parser
# from langchain_core.tools import tool
# from typing import Annotated
# from langgraph.prebuilt import InjectedState
# from .utilities import send_email
# from pytz import timezone
# from dotenv import load_dotenv

# load_dotenv()

# def check_availability(start_time: str, end_time: str, creds) -> bool:
#     """Check if particular time slot is available on Google Calendar."""

#     service = build('calendar', 'v3', credentials=creds)
#     st = parser.parse(start_time).isoformat()
#     en = end_time
#     events = None
#     print(st)
#     print(en)
#     print('------CHECK AVAILABLITY------')
#     try:
#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=st,
#             timeMax=en,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
#         events = events_result.get('items', [])
#     except Exception as e:
#         print(str(e))
#         pass
    
#     if events == None:
#         st = parser.parse(start_time).astimezone(timezone('Asia/Kolkata')).isoformat()
#         en = parser.parse(end_time).astimezone(timezone('Asia/Kolkata')).isoformat()
#         try:
#             events_result = service.events().list(
#                 calendarId='primary',
#                 timeMin=st,
#                 timeMax=en,
#                 singleEvents=True,
#                 orderBy='startTime'
#             ).execute()
#             events = events_result.get('items', [])
#         except Exception as e:
#             print(str(e))
#             raise e
#     print("availibility check hone wala hai")
#     ans = False
#     if not events:
#         ans = True
#     else:
#         ans = False
#     print(ans)
#     return ans

# @tool
# def book_event(time: str, email: str, state: Annotated[dict, InjectedState]) -> str:
#     """
#     Create an event on Google Calendar. This tool requires the following information:
#     - time: The time with date
#     - email: Email to send calendar invite
#     """
    
#     ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
#     title = "Meeting with Vinove"
#     description = "Product discussion"
#     start_time = time
#     if not start_time:
#         missing_fields = []
#         if not start_time: missing_fields.append("time")
#         return f"ERROR: Missing required fields: {', '.join(missing_fields)}. Please collect all required information before booking."
#     print('-------inside of book_event------')
#     try:
#         parser.parse(start_time).astimezone(ist_timezone).isoformat()
#     except ValueError:
#         return "ERROR: Invalid date/time format."

#     creds = None
#     print('=============')
#     print(os.getenv("JTOKEN"))
#     print('=============')
#     creds = Credentials(
#         token=os.getenv("JTOKEN"),
#         refresh_token=os.getenv("JREFRESHTOKEN"),
#         token_uri=os.getenv("JTOKENURI"),
#         client_id=os.getenv("JCLIENTID"),
#         client_secret= os.getenv("JCLIENTSECRECT"),
#     )

#     dt = datetime.datetime.fromisoformat(start_time)
#     dt += datetime.timedelta(hours=1)
#     end_time = dt

#     isAvailable = check_availability(start_time, end_time.isoformat(), creds)
#     print("===========>>>>>",isAvailable)
#     if not isAvailable:
#         raise Exception("time slot already booked, ask for another time")
    
#     print(parser.parse(start_time).isoformat())
#     print(end_time.isoformat())

#     event = {
#         'summary': title,
#         'location': 'Vinove',
#         'description': description,
#         'start': {
#             'dateTime': parser.parse(start_time).isoformat(),
#             'timeZone': 'IST',
#         },
#         'end': {
#             'dateTime': end_time.isoformat(),
#             'timeZone': 'IST',
#         },
#         'attendees': [{'email': email}],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#             ],
#         },
#         'conferenceData': {
#             'createRequest': {
#             'requestId': f"{get_time.time()}"
#             }
#         },
#     }
#     event2 = {
#         'summary': title,
#         'location': 'Vinove',
#         'description': description,
#         'start': {
#             'dateTime': parser.parse(start_time).isoformat()+"+05:30",
#             'timeZone': 'IST',
#         },
#         'end': {
#             'dateTime': end_time.isoformat()+"+05:30",
#             'timeZone': 'IST',
#         },
#         'attendees': [{'email': email}],
#         'reminders': {
#             'useDefault': False,
#             'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#             ],
#         },
#         'conferenceData': {
#             'createRequest': {
#             'requestId': f"{get_time.time()}"
#             }
#         },
#     }
#     service = build("calendar", "v3", credentials=creds)
#     print('=============')
#     booked = False
#     try:
#         event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1, sendUpdates='all', sendNotifications=True).execute()
#         booked = True
#     except Exception as e:
#         raise e
    
#     if not booked:
#         try:
#             event = service.events().insert(calendarId='primary', body=event2, conferenceDataVersion=1, sendUpdates='all', sendNotifications=True).execute()
#             booked = True
#         except Exception as e:
#             raise e
#     print('=============')

#     if booked:
#         try:
#             send_email({
#                 'link': event.get('htmlLink'),
#                 'title': title,
#                 'start_time': parser.parse(start_time).strftime("%d %b %y, %H:%M"),
#                 'end_time': end_time.strftime("%d %b %y, %H:%M"),
#                 'description': description
#             }, state["messages"], email)
#         except:
#             pass
#     return "Event Booked Successfully"



# @tool
# def cancel_Event(time: str) -> str:
#     "You **MUST** use the `cancel_Event` tool after getting the date & time."
#     from datetime import datetime, timedelta, timezone
#     ist = timezone(timedelta(hours=5, minutes=30))
#     print("------Inside cancel-event----")
#     print(f"Received time for cancellation: {time}")

#     if not time:
#         return "Error: No datetime provided for event cancellation."

#     try:
#         start_time = datetime.fromisoformat(time).replace(microsecond=0)
        
#         # start_time_utc = start_time.astimezone(timezone.utc)

#         start_time_ist = start_time.replace(tzinfo=ist)  # Convert input to IST
#         start_time_utc = start_time_ist.astimezone(timezone.utc)  # Convert to UTC
#         end_time_utc = start_time_utc + timedelta(hours=1)

#         creds = Credentials(
#             token=os.getenv("JTOKEN"),
#             refresh_token=os.getenv("JREFRESHTOKEN"),
#             token_uri=os.getenv("JTOKENURI"),
#             client_id=os.getenv("JCLIENTID"),
#             client_secret=os.getenv("JCLIENTSECRECT"),
#         )

#         service = build("calendar", "v3", credentials=creds)

#         print(f"Searching events from {start_time_utc} to {end_time_utc} (UTC)")

#         events_result = service.events().list(
#             calendarId='primary',
#             timeMin=start_time_utc.isoformat(),
#             timeMax=end_time_utc.isoformat(),
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()

#         print(f"Raw events data: {events_result}")
#         all_events = service.events().list(calendarId='primary').execute()
#         print(f"All events: {all_events}")

#         events = events_result.get('items', [])
#         for event in events:
#             print(f"Event ID: {event['id']}, Start Time: {event['start']['dateTime']}")

#         if not events:
#             return f"No event found between {start_time_utc} and {end_time_utc} (UTC)."

#         event_id = events[0]['id']
#         service.events().delete(calendarId='primary', eventId=event_id).execute()
#         return "Event Cancelled Successfully"
    
#     except Exception as e:
#         return f"Error canceling event: {str(e)}"


# if __name__ == "__main__":
#     ist_timezone = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
#     now = datetime.datetime.now(ist_timezone)
#     start_time = (now + datetime.timedelta(hours=61)).isoformat()
#     print(start_time)
#     ans = book_event(start_time)
#     print(ans)

    