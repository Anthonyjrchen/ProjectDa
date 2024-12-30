from typing import Annotated, List
from pydantic import BaseModel
from fastapi import FastAPI, Request, Form
import pandas as pd
import win32com.client as client
from fastapi.middleware.cors import CORSMiddleware

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
test1Calender = None
calendarList = []
# Iterate through NavigationGroups and NavigationFolders
for group in outlook_navmod.NavigationGroups:
    # group.Name is My Calendars, All Group Calendars, etc.
    for folder in group.NavigationFolders:
        calendarList.append(folder.DisplayName)
        # folders are calendars
        # print("> " + folder.DisplayName + ", group:" + str(group.Position) + " position:" + str(folder.Position))
        if folder.DisplayName=="Test 1":
            test1Calender = folder
            print("Found Test 1")
print(test1Calender.Folder.EntryID)
# print(test1Calender.GetIdsOfNames())

# print(dir(namespace)))
# print(namespace.GetFolderFromID(test1Calender.Folder.EntryID))

    # if folder.Name == "Test 1":
    #     test1Calender = folder
    #     print(f"Found Calendar: {test1Calender.Name}")
    #     break  # Exit the loop once found

actual_folder = namespace.GetFolderFromID(test1Calender.Folder.EntryID)
# print(dir(actual_folder.Items))
# # print(actual_folder.Items)



# to display calendars, use:
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
    categories: List[str]  # List of selected categories

@app.post("/add")
async def add(userEvent:EventData):
    event = actual_folder.Items.Add()
    event.subject = userEvent.eventName
    event.body = "Just a test"
    event.AllDayEvent = True
    event.start = event.date # Ensure date is formatted as e.g. 2018-01-09)
    event.save() 
    return {
        "message": "Event added successfully",
        "event": userEvent
    }

@app.get("/calendars")
def getCalendars(request: Request):
    # print(calendarList)
    return calendarList