from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
import pandas as pd
import win32com.client as client
from fastapi.middleware.cors import CORSMiddleware
import calculator
import time
import uvicorn
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
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
storeIdDict = {}
progress = 0
with open("recipientList.txt", 'w') as f:
    f.write("")
    f.close()
ignoredCalendars = open("ignoreCalendars.txt","r").read().split("\n")
lawyerCalendars = open("lawyerCalendars.txt","r").read().split("\n")


# Iterate through NavigationGroups and NavigationFolders
for group in outlook_navmod.NavigationGroups:
    # group.Name is My Calendars, All Group Calendars, etc.
    if group.Name != "Shared Calendars":
        for folder in group.NavigationFolders:
            if folder.DisplayName not in ignoredCalendars:
                calendarName = str(folder.Folder.FolderPath).split("\\")[-1]+"("+str(folder.Folder.FolderPath).split("\\")[2]+")"
                storeIdDict[calendarName] = folder.Folder.StoreID
                calendarList.append(calendarName)
                try:
                    calendarDict[calendarName] = namespace.GetFolderFromID(folder.Folder.EntryID)
                except:
                    print("Could not find folder for " + folder.DisplayName)
    else:
        #try using GetSharedFolderFromID
        #Add to recipient list
        for folder in group.NavigationFolders:
            if folder.DisplayName not in ignoredCalendars:
                if " - " in folder.DisplayName:
                    calendarList.append(folder.DisplayName.split(" - ")[1])
                    storeIdDict[folder.DisplayName.split(" - ")[1]] = folder.Folder.StoreID
                else:
                    calendarList.append(folder.DisplayName)
                    storeIdDict[folder.DisplayName] = folder.Folder.StoreID
                
                with open("recipientList.txt", 'a+') as f:
                            if " - " in folder.DisplayName:
                                f.write(folder.DisplayName.split(" - ")[1]+"\n")
                            else:
                                f.write(folder.DisplayName + "\n")
                            f.close()
recipients = open("recipientList.txt","r").read().split("\n")
for name in recipients:
    recipient = namespace.CreateRecipient(name)
    if recipient.Resolve():
        try:
            calendarDict[name] = namespace.GetSharedDefaultFolder(recipient,9)
        except:
            print("Couldn't resolve recipient: " + name)
eventDict = {}

@app.get("/")
async def root():
    return "Backend is up and running"

class initData(BaseModel):
    date: str  # Date in the format YYYY-MM-DD
    calendars: List[str]  # List of selected categories

@app.post("/initiateAdd")
async def add(userEvent:initData):
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
    return {
        "splitDate":splitDate,
        "eventDict":eventDict,
        "validCalendars":validCalendars,
        } 

class Event(BaseModel):
    targetFolder:str
    courtFileNum:str
    jmlFileNum:str
    styleOfCause:str
    eventDate:List[str]
    formName: str
    plaintiffDefendant: bool

@app.post("/add")
async def addEvent(e:Event):
    event = calendarDict[e.targetFolder].Items.Add()
    if e.plaintiffDefendant:
        event.subject = e.jmlFileNum + " " + e.styleOfCause + " - " + e.eventDate[0] + " DUE - " + e.formName
    else:
        event.subject = e.jmlFileNum + " " + e.styleOfCause + " - DUE - " + e.formName
    event.body = "This is an automatically generated event using ProjectDA."
    event.location = "DAhandler - " + e.courtFileNum
    event.AllDayEvent = True
    event.start = e.eventDate[1] # Ensure date is formatted as e.g. 2018-01-09
    event.save()
    
@app.post("/add/reminder")
async def addEventReminder(e:Event):
    event = calendarDict[e.targetFolder].Items.Add()
    if e.plaintiffDefendant:
        event.subject = e.jmlFileNum + " " + e.styleOfCause + " - " + e.eventDate[0] + " DUE - " + e.formName
    else:
        event.subject = e.jmlFileNum + " " + e.styleOfCause + " - " + e.eventDate[0] + " until DUE - " + e.formName
    event.body = "This is an automatically generated event using ProjectDA."
    event.location = "DAhandler - " + e.courtFileNum
    event.AllDayEvent = True
    event.start = e.eventDate[1] # Ensure date is formatted as e.g. 2018-01-09
    event.save() 

def inputEventDates(dates):
    eventDict["NOTICE TO MEDIATE, FORM 1"] = [["",dates["date1"]],["1 month",dates["rm1_date1"]],["2 weeks",dates["rm2_date1"]],["1 week",dates["rm3_date1"]],["1 day",dates["rm4_date1"]]]
    
    eventDict["EXPERT'S REPORT"] = [["",dates["date2"]],["1 month",dates["rm1_date2"]],["2 weeks",dates["rm2_date2"]],["1 week",dates["rm3_date2"]],["1 day",dates["rm4_date2"]]]

    eventDict["EXAMINATIONS FOR DISCOVERY"] = [["",dates["date3"]],["2 months",dates["rm1_date3"]],["1 month",dates["rm2_date3"]],["2 weeks",dates["rm3_date3"]],["1 week",dates["rm4_date3"]],["1 day",dates["rm5_date3"]]]

    eventDict["TRIAL BRIEF, FORM 41(P)"] = [["PLAINTIFF",dates["date4"]],["1 month until PLAINTIFF",dates["rm1_date4"]],["1 week until PLAINTIFF",dates["rm2_date4"]]]

    eventDict["TRIAL BRIEF, FORM 41(D)"] = [["DEFENDANT",dates["date5"]],["1 month until DEFENDANT",dates["rm1_date5"]],["1 week until DEFENDANT",dates["rm2_date5"]]]

    eventDict["NOTICE TO ADMIT, FORM 23"] = [["",dates["date6"]],["1 month",dates["rm1_date6"]],["2 weeks",dates["rm2_date6"]],["1 week",dates["rm3_date6"]],["1 day",dates["rm4_date6"]]]

    eventDict["RESPONDING REPORTS"] = [["",dates["date7"]],["1 month",dates["rm1_date7"]],["2 weeks",dates["rm2_date7"]],["1 week",dates["rm3_date7"]],["1 day",dates["rm4_date7"]]]

    eventDict["TRIAL MANAGEMENT CONFERENCE"] = [["",dates["date8"]],["4 months",dates["rm1_date8"]],["3 months", dates["rm2_date8"]],["2 months",dates["rm3_date8"]],["1 month",dates["rm4_date8"]],["2 weeks", dates["rm5_date8"]],["1 week", dates["rm6_date8"]]]
    
    eventDict["NOTICE OF OBJECTION"] = [["",dates["date9"]],["1 month",dates["rm1_date9"]],["2 weeks",dates["rm2_date9"]],["1 week",dates["rm3_date9"]],["1 day",dates["rm4_date9"]]]

    eventDict["TRIAL RECORD"] = [["",dates["date10"]],["1 month",dates["rm1_date10"]],["2 weeks",dates["rm2_date10"]],["1 week",dates["rm3_date10"]]]
    eventDict["TRIAL CERTIFICATE, FORM 42"] = [["",dates["date11"]],["1 month",dates["rm1_date11"]],["2 weeks",dates["rm2_date11"]],["1 week",dates["rm3_date11"]]]
    eventDict["NOTICE OF EXAMINATION"] = [["",dates["date12"]],["1 month",dates["rm1_date12"]],["2 weeks",dates["rm2_date12"]],["1 week",dates["rm3_date12"]]]
    eventDict["INSPECTION OF PHOTOGRAPHS, ETC."] = [["",dates["date13"]],["1 month",dates["rm1_date13"]],["2 weeks",dates["rm2_date13"]],["1 week",dates["rm3_date13"]]]
    eventDict["NOTICE TO PRODUCE, FORM 43"] = [["",dates["date14"]],["1 month",dates["rm1_date14"]],["2 weeks",dates["rm2_date14"]],["1 week",dates["rm3_date14"]]]
    return eventDict #eventDict contains all event dates and reminder dates i..e {"Notice to Mediate, Form 1":["23-Aug-2024","23-Jul-2024","9-Aug-2024","16-Aug-2024","22-Aug-2024",]} First date is the due date, next x dates are reminder dates.

class initDeleteObject(BaseModel):
    caseNum:str
    calendars: List[str]

@app.post("/initDelete")
async def delete(initDeleteObject:initDeleteObject):
    t0 = time.time()
    deleteDict = {}
    caseNum ="DAhandler - " + str(initDeleteObject.caseNum.strip())
    for calendar in initDeleteObject.calendars:
        x = calendarDict[calendar]
        items = x.Items
        
        itemsToDelete = []
        for i in range(items.Count, 0, -1):
            if items.Item(i).location == caseNum:
                itemsToDelete.append(items.Item(i).EntryID)
        deleteDict[calendar] = itemsToDelete
        print("Found " + str(len(itemsToDelete)) + " items to delete in " + calendar)
    t1 = time.time()

    print(t1-t0)
    return {"deleteDict":deleteDict}

class deleteEvent(BaseModel):
    caseNum: str
    calendar: str
    curItem: str
listToDelete = []
@app.post("/planDelete")
async def deleteEvent(deleteEvent: deleteEvent):
    listToDelete = []
    caseNum ="DAhandler - " + str(deleteEvent.caseNum.strip())
    items = calendarDict[deleteEvent.calendar].Items
    if items.Item(deleteEvent.curItem).location == caseNum:
        # print("Deleting " + items.Item(deleteEvent.curItem).subject + "...")
        # items.Item(deleteEvent.curItem).delete()
        listToDelete.append(deleteEvent.curItem)
    return {"message":"successful"}

class trueDelete(BaseModel):
    calendar:str
    curItem:str

@app.post("/delete")
async def trueDelete(trueDelete:trueDelete):
    items = calendarDict[trueDelete.calendar].Items
    # items.Item(int(trueDelete.curItem)).delete()
    # .GetItemFromID(items.Item(int(trueDelete.curItem)).EntryID).subject
    targetCalendar = calendarDict[trueDelete.calendar]
    namespace.GetItemFromID(trueDelete.curItem,storeIdDict[trueDelete.calendar]).delete()
    return

@app.get("/storeIDs")
def getStoreIDs():
    return storeIdDict

@app.get("/calendars")
def getCalendars():
    return {"calendarList":calendarList}

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
async def testCalcDates(year:str,month:str,day:str):
    return calc_dates(year,month,day)

'''
lawyerCalendar functions
'''
@app.get("/lawyerCalendars/update")
def updateLayerCalendars():
    return open("lawyerCalendars.txt","r").read().split("\n")

'''
setting functions
'''
@app.get("/settings")
def retrieveSettings():
    with open("holidays.txt", "r") as f1:
        holidays = f1.read()
    with open("ignoredCalendars.txt", "r") as f2:
        ignoredCalendars = f2.read()
    with open("lawyerCalendars.txt", "r") as f3:
        lawyerCalendars = f3.read()
    
    return {"holidays": holidays, "ignoredCalendars": ignoredCalendars, "lawyerCalendars": lawyerCalendars}

@app.get("/settings/update")
def updateSettings(holidays:str,ignoredCalendars:str,lawyerCalendars:str):
    with open("holidays.txt", "w") as f1:
        f1.write(holidays)
    with open("ignoredCalendars.txt", "w") as f2:
        f2.write(ignoredCalendars)
    with open("lawyerCalendars.txt", "w") as f3:
        f3.write(lawyerCalendars)

'''
contact support route
'''
@app.get("/support/contact")
async def contactSupport(subject:str,body:str):
    #email support email
    print("at least started the contactSupport method")
    recipients = ["anthonyjrchen@gmail.com","danangelaneria@gmail.com"]
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "meepmoop1322@gmail.com"
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp_server:
        smtp_server.login("meepmoop1322@gmail.com","iwkw onob xprd lhad")
        smtp_server.sendmail("meepmoop1322@gmail.com",recipients,msg.as_string()) 
    return subject + "-" + body

def serve():
    """Serve the web application."""
    uvicorn.run(app, port=8000)

if __name__ == "__main__":
    serve()