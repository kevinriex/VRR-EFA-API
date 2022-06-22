import aiohttp
import asyncio
from datetime import datetime
import json


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
        "Ratingen", "Perkerhof", now
    )
    #print(json.dumps(departures))
    line = departures["departureList"][0]["servingLine"]["number"]
    route = departures["departureList"][0]["servingLine"]["direction"]
    deptime = getDateTime(departures["departureList"][0]["dateTime"])
    
    if departures["departureList"][0]["servingLine"]["delay"] != "0":
        delay = departures["departureList"][0]["servingLine"]["delay"]
        print(line, route, deptime, delay) 
    else:
        print(line, route, deptime)

def getDateTime(data):
    year = data["year"]
    month = data["month"]
    weekday =  data["day"]
    day = data["weekday"]
    hour = data["hour"]
    minute = data["minute"]
    return f"{day}.{month}.{year} {hour}:{minute}"

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())