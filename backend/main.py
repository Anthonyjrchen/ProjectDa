from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
import pandas as pd
import win32com.client as client
from fastapi.middleware.cors import CORSMiddleware
import calculator
import time
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://anthonyjrchen.github.io/ProjectDa",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Updated server")
outlook = client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
calendarFolder = namespace.GetDefaultFolder(9)
outlook_navpane = client.Dispatch('Outlook.Application').ActiveExplorer().NavigationPane
outlook_navmod = outlook_navpane.Modules.getNavigationModule(1)
calendarList = []
calendarDict = {}
with open("recipientList.txt", 'w') as f:
    f.write("")
ignoredCalendars = open("ignoreCalendars.txt","r").read().split("\n")

# Iterate through NavigationGroups and NavigationFolders
for group in outlook_navmod.NavigationGroups:
    # group.Name is My Calendars, All Group Calendars, etc.
    if group.Name != "Shared Calendars":
        for folder in group.NavigationFolders:
            if folder.DisplayName not in ignoredCalendars:
                calendarList.append(str(folder.Folder.FolderPath).split("\\")[-1]+"("+str(folder.Folder.FolderPath).split("\\")[2]+")")
                try:
                    calendarDict[str(folder.Folder.FolderPath).split("\\")[-1]+"("+str(folder.Folder.FolderPath).split("\\")[2]+")"] = namespace.GetFolderFromID(folder.Folder.EntryID)
                except:
                    print("Could not find folder for " + folder.DisplayName)
    else:
        #try using GetSharedFolderFromID
        #Add to recipient list
        for folder in group.NavigationFolders:
            if folder.DisplayName not in ignoredCalendars:
                if " - " in folder.DisplayName:
                    calendarList.append(folder.DisplayName.split(" - ")[1])
                else:
                    calendarList.append(folder.DisplayName)
                
                with open("recipientList.txt", 'a+') as f:
                            if " - " in folder.DisplayName:
                                f.write(folder.DisplayName.split(" - ")[1]+"\n")
                            else:
                                f.write(folder.DisplayName + "\n")
                            f.close()
recipients = open("recipientList.txt","r").read().split("\n")
for recipient in recipients:
    try:
        calendarDict[recipient] = namespace.GetSharedDefaultFolder(namespace.CreateRecipient(recipient),9)
    except:
        print("Finished scanning recipientList")
eventDict = {}

@app.get("/")
async def root():
    return "Backend is up and running"

class EventData(BaseModel):
    date: str  # Date in the format YYYY-MM-DD
    jmlFileNum: str
    courtFileNum: str
    styleOfCause: str
    calendars: List[str]  # List of selected categories

class deleteEvent(BaseModel):
    caseNum: str
    calendars: List[str]

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
        print(calendarDict)
        return {"error":str(invalidCalendars) + " was not able to be added to"}
    splitDate = userEvent.date.split("-")
    inputEventDates(calc_dates(splitDate[0],splitDate[1],splitDate[2])) #fills the global eventDict variable with events and their due/reminder dates
    eventDictKeys = eventDict.keys()
    #for each valid calendar, traverse eventDict and add events and event reminders
    for calendar in validCalendars:
        for eventKey in eventDictKeys:
            eventDates = eventDict[eventKey]
            addEvent(calendarDict[calendar],userEvent.courtFileNum, userEvent.jmlFileNum, userEvent.styleOfCause,eventDates.pop(0), eventKey) #add due dates (lawyers and paralegal and self) (targetFolder, courtFileNum, jmlFileNum, styleOfCause, eventDate, formName) is the format for calling addEvent
            for reminderDay in eventDates:
                addEvent(calendarDict[calendar],userEvent.courtFileNum, userEvent.jmlFileNum, userEvent.styleOfCause,reminderDay, eventKey + " Reminder") #add due dates and reminders (lawyers and paralegal and self)        
    return {
        "message": "Event added successfully",
        "event": userEvent,
        "validCalendars": validCalendars,
    }

def addEvent(targetFolder, courtFileNum, jmlFileNum, styleOfCause, eventDate, formName):
    event = targetFolder.Items.Add()
    event.subject = jmlFileNum + " " + styleOfCause + " " + formName
    event.body = "This is an automatically generated event using ProjectDA."
    event.location = "DAhandler - " + courtFileNum
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

@app.post("/delete")
async def delete(deleteEvent: deleteEvent):
    t0 = time.time()
    caseNum ="DAhandler - " + str(deleteEvent.caseNum.strip())
    for calendar in deleteEvent.calendars:
        x = calendarDict[calendar]
        items = x.Items
        for i in range(items.Count, 0, -1):
            if items.Item(i).location == caseNum:
                print("Deleting " + items.Item(i).subject + "...")
                items.Item(i).delete()
        print("Done deleting for: " + calendar)

    # for paralegal in paralegals:
    #     x = get_calendar(paralegal)
    #     items = x.Items
    #     for i in range(items.Count, 0, -1):
    #         if items.Item(i).body.strip() == file.strip():
    #             print("Deleting " + items.Item(i).subject + "...")
    #             items.Item(i).delete()
    #     print("Done deleting for: " + paralegal)

    # items = namespace.GetDefaultFolder(9).Items
    # for i in range(items.Count, 0, -1):
    #     if items.Item(i).body.strip() == file.strip():
    #         print("Deleting " + items.Item(i).subject + "...")
    #         items.Item(i).delete()
    # print("Done deleting for main calendar")
    
    t1 = time.time()

    print(t1-t0)
    return {"message":"Deleted Successfully"}

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

def serve():
    """Serve the web application."""
    uvicorn.run(app, port=8000)

if __name__ == "__main__":
    serve()