from typing import Annotated, List
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
import pandas as pd
import win32com.client as client
from fastapi.middleware.cors import CORSMiddleware
import calculator

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




outlook = client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
for a in namespace.Folders:
    print(a)
calendarFolder = namespace.GetDefaultFolder(9)
outlook_navpane = client.Dispatch('Outlook.Application').ActiveExplorer().NavigationPane
outlook_navmod = outlook_navpane.Modules.getNavigationModule(1)
calendarList = []
calendarDict = {}
# Iterate through NavigationGroups and NavigationFolders
for group in outlook_navmod.NavigationGroups:
    # group.Name is My Calendars, All Group Calendars, etc.
    for folder in group.NavigationFolders:
        calendarList.append(folder.DisplayName)
        calendarDict[folder.DisplayName] = namespace.GetFolderFromID(folder.Folder.EntryID)

eventDict = {}

# for idx, a in enumerate(calendarFolder.Folders):
#     calendarList.append(a.Name)
#     print("appending " + a.Name)
#     if a.Name=="Test 1":
#         test1Calender = a

# this is for testing
# targetFolder = None
# if recipient.Resolve():
#     targetFolder = namespace.GetDefaultFolder("Test 1",9)
# else:
#     raise Exception("No Recipient Found for name: " + "Test 1")
# print(calendarFolder.Folders)

@app.get("/")
async def root():
    
    return {"message": "Hello World"}

class EventData(BaseModel):
    date: str  # Date in the format YYYY-MM-DD
    eventName: str
    calendars: List[str]  # List of selected categories

@app.post("/add")
async def add(userEvent:EventData):
    # find calendar(s)
    targetCalendars = userEvent.calendars
    validCalendars = []
    invalidCalendars = []
    for calendar in targetCalendars:
        if calendar in calendarDict:
            validCalendars.append(calendar)
        else:
            invalidCalendars.append(calendar)
    if invalidCalendars:
        return {"error":invalidCalendars}

    inputEventDates(string_dates)

    # create and add event to every calendar
    for calendar in validCalendars:
        addEvent(calendarDict[calendar],userEvent.eventName, userEvent.date)
        
    return {
        "message": "Event added successfully",
        "event": userEvent,
        "validCalendars": validCalendars,
    }

def addEvent(targetFolder, eventName, eventDate):
    event = targetFolder.Items.Add()
    event.subject = eventName
    event.body = "Just a test"
    event.AllDayEvent = True
    event.start = eventDate # Ensure date is formatted as e.g. 2018-01-09)
    event.save() 

@app.get("/calendars")
def getCalendars(request: Request):
    # print(calendarList)
    return calendarList

'''
CALCULATOR FUNCTION
'''
def calc_dates(year,month,day):
    raw_dates = calculator.calculate_dates(year,month,day)
    string_dates = {}
    for key,date in raw_dates.items():
        month = calculator.months2[str(date.month)]
        string_dates[key] = str(date.day) + "-" + month + "-" + str(date.year)

    return string_dates



@app.get("/calcDates")
def testCalcDates():
    return calc_dates("2024","December","24")