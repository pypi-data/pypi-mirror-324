import uuid
from datetime import datetime
import tempfile

def truncate(string, width):
    if len(string) > width:
        string = string[:width-3] + '...'
    return string

class ICalHandler:

    def __init__(self, content):
        self.content = content

    def make_ical(self):
        file = tempfile.gettempdir() + "/" + str(uuid.uuid4()) + ".ics"
        f = open(file, "w")
        f.write("""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//github.com//totorocodesoften//ultoical
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Europe/Paris
LAST-MODIFIED:20240422T053451Z
TZURL:https://www.tzurl.org/zoneinfo-outlook/Europe/Paris
X-LIC-LOCATION:Europe/Paris
BEGIN:DAYLIGHT
TZNAME:CEST
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZNAME:CET
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
""".replace("\n", "\r\n"))
        dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        for event in self.content:
            start = event["startDateTime"].replace("+01:00", "").replace(":", "").replace("-", "")
            end = event["endDateTime"].replace("+01:00", "").replace(":", "").replace("-", "")
            teacher = event["teachers"][0]["displayname"] if len(event["teachers"]) > 0 else ""
            room = event["rooms"][0] if len(event["rooms"]) > 0 else {"label": "", "building": ""}
            desc = "{0:<10s}".format(truncate(event["course"]["label"] + " " + room["label"] + " " + teacher, 60))

            f.write(f"""BEGIN:VEVENT
DTSTAMP:{dtstamp}
UID:{uuid.uuid4()}@ultoical.totorocodesoften
DTSTART;TZID=Europe/Paris:{start}
DTEND;TZID=Europe/Paris:{end}
SUMMARY:{"{0:<10s}".format(truncate(event["course"]["label"], 65))}
URL:{event["course"]["url"]}
DESCRIPTION:{desc}
LOCATION:{room["label"]}, {room["building"]}
CLASS:PRIVATE
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:{"{0:<10s}".format(truncate(event["course"]["label"], 30))} is soon, go to {room["label"]}
TRIGGER:-PT5M
END:VALARM
END:VEVENT
""".replace("\n", "\r\n"))
        f.write("END:VCALENDAR")
        f.close()
        # get the path from the oppened file
        return file