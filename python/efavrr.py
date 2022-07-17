import aiohttp
import asyncio
from datetime import datetime
import json
import pytz
import terminaltables
import os
from sys import argv

timezone = pytz.timezone('Europe/Berlin')
datetime_format = "%d.%m.%Y %H:%M"

class EFA:
    def __init__(self, url, proximity_search=False):
        self.dm_url = url + "/XML_DM_REQUEST"
        self.dm_post_data = {
            "language": "de",
            "mode": "direct",
            "outputFormat": "JSON",
            "type_dm": "stop",
            "useProxFootSearch": "0",
            "useRealtime": "1",
        }

        if proximity_search:
            self.dm_post_data["useProxFootSearch"] = "1"

    async def get_departures(self, place, name, ts):
        self.dm_post_data.update(
            {
                "itdDateDay": ts.day,
                "itdDateMonth": ts.month,
                "itdDateYear": ts.year,
                "itdTimeHour": ts.hour,
                "itdTimeMinute": ts.minute,
                "name_dm": name,
            }
        )
        if place is None:
            self.dm_post_data.pop("place_dm", None)
        else:
            self.dm_post_data.update({"place_dm": place})
        departures = list()
        async with aiohttp.ClientSession() as session:
            async with session.post(self.dm_url, data=self.dm_post_data) as response:
                # EFA may return JSON with a text/html Content-Type, which response.json() does not like.
                departures = json.loads(await response.text())
        return departures


async def main():
    now = datetime.now()
    departures = await EFA("https://efa.vrr.de/standard/").get_departures(
        city, station, now
    )
    #print(json.dumps(departures))
    #with open('data.json', 'w') as outfile:
     #   json.dump(departures, outfile)
    return departures



def display(departures):
    line = departures["departureList"][0]["servingLine"]["number"]
    route = departures["departureList"][0]["servingLine"]["direction"]
    deptime = getDateTime(departures["departureList"][0]["dateTime"])
    
    if departures["departureList"][0]["servingLine"]["delay"] != "0":
        delay = departures["departureList"][0]["servingLine"]["delay"]
        print(line, route, deptime, delay) 
    else:
        print(line, route, deptime)
    
def displayall(departures):
    stop = departures["dm"]["points"]["point"]["name"]
    print(f"departures for: { stop }")
    for departure in departures["departureList"]:
        line = departure["servingLine"]["number"]
        route = departure["servingLine"]["direction"]
        deptime = getDateTime(departure["dateTime"]) # realDateTime = Incl Verstpätung, dateTime = Fahrplan
        platform = departure["platformName"]
        if "delay" in departure["servingLine"]:
            delay = departure["servingLine"]["delay"]
        else:
            delay = 0
        commingin = deptime - getCurrentDate()
        countdown = departure["countdown"]

        if len(countdown) < 2:
            countdown = "0" + countdown

        if int(countdown) < 1:
            print(line, route, platform, deptime.strftime(datetime_format),delay, "sofort")
        if int(countdown) > 0 and int(countdown) < 60:
            print(line, route, platform, deptime.strftime(datetime_format), delay, f"in: {countdown} min")
        if int(countdown) < 120 and int(countdown) > 60:
            print(line, route, platform, deptime.strftime(datetime_format), delay)

def getCurrentDate():
    now = datetime.now(timezone)
    return datetime(year=int(now.year),month=int(now.month),day=int(now.day),hour=int(now.hour),minute=int(now.minute),tzinfo=timezone)

def getDateTime(data):
    year = data["year"]
    month = data["month"]
    weekday =  data["weekday"]
    day = data["day"]
    hour = data["hour"]
    minute = data["minute"]

    if len(hour) < 2:       #CHANGE!!!
        hour = "0" + hour
    if len(minute) < 2:
        minute = "0" + minute
    if len(day) < 2:
        day = "0" + day
    if len(month) < 2:
        month = "0" + month

    date = datetime(year=int(year),month=int(month),day=int(day),hour=int(hour),minute=int(minute),tzinfo=timezone)
    #date = datetime.strptime(f"{day}.{month}.{year} {hour}:{minute}", "%d.%m.%Y %H:%M")
    return date

def displayalltable(rawdata):
    header = [["line","destination","platform","depature","delay","countdown"]]
    data = list(header)
    for departure in rawdata["departureList"]:
        line = departure["servingLine"]["number"]
        route = departure["servingLine"]["direction"]

        #realDateTime = Incl Verstpätung, dateTime = Fahrplan
        if "realDateTime" in departure:
            deptime = getDateTime(departure["realDateTime"])
        else:
            deptime = getDateTime(departure["dateTime"])
        platform = departure["platformName"]
        if "delay" in departure["servingLine"]:
            delay = departure["servingLine"]["delay"]
        else:
            delay = 0
        
        countdown = departure["countdown"]
        if len(countdown) < 2:
            countdown = "0" + countdown
        
        if int(countdown) < 1:
            package = [line,route,platform,deptime.strftime(datetime_format),delay,"now"]
            data.append(package)
        if int(countdown) > 0 and int(countdown) < 60:
            package = [line, route, platform, deptime.strftime(datetime_format), delay, f"in: {countdown} min"]
            data.append(package)
        if int(countdown) < 120 and int(countdown) > 60:
            package = [line, route, platform, deptime.strftime(datetime_format), delay]
            data.append(package)

    table = terminaltables.AsciiTable(data, title=rawdata["dm"]["points"]["point"]["name"])
    print(table.table)

def doc():
    print("\nCorrect usage of this command\n")
    print("Version 1: departures [Station]")
    print("     In this case the city is 'Ratingen'")
    print("Version 2: departures [CITY] [STATION]")
    print("     In this case the city and station are given.")

def start():
    data = asyncio.run(main())
    #displayall(data)
    displayalltable(data)

if __name__ == "__main__":
    '''if asyncio.get_event_loop().is_running():
        data = asyncio.get_event_loop().run_until_complete(main())
    else:
        loop = asyncio.new_event_loop()
        data = loop.run_until_complete(main())'''
    
    if len(argv) == 1:
        print("You have to provide at least one argument...")
        doc()
    if len(argv) == 2:
        print("The city is now 'Ratingen'.")
        city = "Ratingen"
        station = argv[1]
        start()
    if len(argv) == 3:
        city = argv[1]
        station = argv[2]
        start()
    if len(argv) >= 4:
        print("Too many arguments...")
        doc()
    
    os.system("pause")