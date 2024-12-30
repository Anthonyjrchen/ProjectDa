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
    splitDate = userEvent.date.split("-")
    inputEventDates(calc_dates(splitDate[0],splitDate[1],splitDate[2])) #fills the global eventDict variable with events and their due/reminder dates
    eventDictKeys = eventDict.keys()
    #for each valid calendar, traverse eventDict and add events and event reminders
    for calendar in validCalendars:
        for eventKey in eventDictKeys:
            eventDates = eventDict[eventKey]
            addEvent(calendarDict[calendar],eventKey,eventDates.pop(0)) #add due dates (lawyers and paralegal and self)
            for reminderDay in eventDates:
                addEvent(calendarDict[calendar],eventKey + " Reminder",reminderDay) #add due dates and reminders (lawyers and paralegal and self)

    # for calendar in validCalendars:
    #     addEvent(calendarDict[calendar],userEvent.eventName, userEvent.date)
        
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

def inputEventDates(dates):
    eventDict["NOTICE TO MEDIATE, FORM 1"] = [dates["date1"],dates["rm1_date1"],dates["rm2_date1"],dates["rm3_date1"],dates["rm4_date1"]]
    eventDict["EXPERT'S REPORT"] = [dates["date2"],dates["rm1_date2"],dates["rm2_date2"],dates["rm3_date2"],dates["rm4_date2"]]
    eventDict["EXAMINATIONS FOR DISCOVERY"] = [dates["date3"],dates["rm1_date3"],dates["rm2_date3"],dates["rm3_date3"],dates["rm4_date3"],dates["rm5_date3"]]
    eventDict["TRIAL BRIEF, FORM 41, PLAINTIFF"] = [dates["date4"],dates["rm1_date4"],dates["rm2_date4"]]
    eventDict["TRIAL BRIEF, FORM 41, OP"] = [dates["date5"],dates["rm1_date5"],dates["rm2_date5"]]
    eventDict["NOTICE TO ADMIT, FORM 23"] = [dates["date6"],dates["rm1_date6"],dates["rm2_date6"],dates["rm3_date6"],dates["rm4_date6"]]
    eventDict["RESPONDING REPORTS"] = [dates["date7"],dates["rm1_date7"],dates["rm2_date7"],dates["rm3_date7"],dates["rm4_date7"]]
    eventDict["TRIAL MANAGEMENT CONFERENCE"] = [dates["date8"],dates["rm1_date8"],dates["rm2_date8"],dates["rm3_date8"],dates["rm4_date8"],dates["rm5_date8"],dates["rm6_date8"]]
    eventDict["NOTICE OF OBJECTION"] = [dates["date9"],dates["rm1_date9"],dates["rm2_date9"],dates["rm3_date9"],dates["rm4_date9"]]
    eventDict["TRIAL RECORD"] = [dates["date10"],dates["rm1_date10"],dates["rm2_date10"],dates["rm3_date10"]]
    eventDict["TRIAL CERTIFICATE, FORM 42"] = [dates["date11"],dates["rm1_date11"],dates["rm2_date11"],dates["rm3_date11"]]
    eventDict["NOTICE OF EXAMINATION"] = [dates["date12"],dates["rm1_date12"],dates["rm2_date12"],dates["rm3_date12"]]
    eventDict["INSPECTION OF PHOTOGRAPHS, ETC."] = [dates["date13"],dates["rm1_date13"],dates["rm2_date13"],dates["rm3_date13"]]
    eventDict["NOTICE TO PRODUCE, FORM 43"] = [dates["date14"],dates["rm1_date14"],dates["rm2_date14"],dates["rm3_date14"]]
    return eventDict #eventDict contains all event dates and reminder dates i..e {"Notice to Mediate, Form 1":["23-Aug-2024","23-Jul-2024","9-Aug-2024","16-Aug-2024","22-Aug-2024",]} First date is the due date, next x dates are reminder dates.

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