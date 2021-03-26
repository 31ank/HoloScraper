import requests
import re
import database

from datetime import datetime
from stream import StreamEntry
from bs4 import BeautifulSoup
from time import sleep

def GetNewData():
    print("Getting new data " + datetime.now().strftime("%H:%M:%S"))
    resp = requests.get('https://schedule.hololive.tv/')
    if resp.ok:
        allEntrys = []
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.find_all("div", class_="row")
        currentDate = ""
        date = datetime.now()
        year = date.strftime("%Y")
        for row in rows:
            rowText = row.text
            rowDate = re.findall(r'[0-1][0-9]/[0-3][0-9]', rowText)
            # Found valid date
            if(any(rowDate) and len(rowDate) == 1):
                currentDate = rowDate[0]
            entrys = row.find_all("a", class_="thumbnail")
            if currentDate:
                for entry in entrys:
                    entryText = entry.text
                    time = re.findall(r'[0-9][0-9]:[0-9][0-9]', entryText)
                    name = re.findall(r'Amelia|Calli|Kiara|Gura|Ina', entryText)
                    if(any(name)):
                        date = year + "-" + currentDate[0:2] + "-" + currentDate[3:5] + " " + time[0][0:2] + ":" + time[0][3:5] + ":00"
                        streamEntry = StreamEntry(name[0], date)
                        allEntrys.append(streamEntry)
        reducedEntrys = []
        for entry in allEntrys:
            if entry not in reducedEntrys:
                reducedEntrys.append(entry)
        for entry in reducedEntrys:
            result = database.InsertEntry(entry)
            print(entry)
            print("added: " + str(result))
    else:
        print('Encountered error while fetching data')
        print(resp.status_code)
        print(resp.text)

# waste time to keep python running -> change to cron jobs?
def main():
    while True:
        try:
            GetNewData()
        except Exception as err:
            print('Error updating data: ' + err)
        # check every 60min for new updates
        sleep(3600)

if  __name__ =='__main__':
    main()