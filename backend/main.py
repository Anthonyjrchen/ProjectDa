from fastapi import FastAPI, Request
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
calendarFolder = namespace.GetDefaultFolder(9)
outlook_navpane = client.Dispatch('Outlook.Application').ActiveExplorer().NavigationPane
outlook_navmod = outlook_navpane.Modules.getNavigationModule(1)
test1Calender = None
# Iterate through NavigationGroups and NavigationFolders
for group in outlook_navmod.NavigationGroups:
    # group.Name is My Calendars, All Group Calendars, etc.
    print(group.Name)
    for folder in group.NavigationFolders:
        # folders are calendars
        print("> " + folder.DisplayName + ", group:" + str(group.Position) + " position:" + str(folder.Position))
        if folder.DisplayName=="Test 1":
            # test1Calender = folder
            print("Found Test 1")


# to display calendars, use:
calendarList = []
for idx, a in enumerate(calendarFolder.Folders):
    calendarList.append(a.Name)
    if a.Name=="Test 1":
        test1Calender = a
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

@app.post("/add")
async def add(request: Request):
    event = test1Calender.Items.Add(1)
    event.subject = request.headers["Subject"]
    event.body = "Just a test"
    event.AllDayEvent = True
    event.start = request.headers["date"]
    event.save() 
    return {"message": "Successful"}

@app.get("/calendars")
def getCalendars(request: Request):
    return calendarList