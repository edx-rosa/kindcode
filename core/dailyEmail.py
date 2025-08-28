import os
import requests
from ics import Calendar
from django.utils import timezone
import random

def getMission():
    return "Live with intention, serve life, and create kindly."

def getQuoteOfTheDay():
    quotes = [
        ("The future depends on what you do today.", "Mahatma Gandhi"),
        ("Wherever you are, be there totally.", "Eckhart Tolle"),
        ("Small deeds done are better than great deeds planned.", "Peter Marshall"),
    ]
    q, a = random.choice(quotes)
    return {"text": q, "author": a}

def getTodayAppointments():
    url = os.getenv("GOOGLE_ICAL_URL", "")
    if not url:
        return []  # no calendar configured yet

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception:
        # If fetch fails, don’t crash the email; just show nothing for today
        return []

    cal = Calendar(resp.text)

    today = timezone.localdate()
    tz = timezone.get_current_timezone()
    items = []

    for event in cal.events:
        # event.begin is an Arrow object; convert to your local tz
        startLocal = event.begin.to(str(tz))
        eventDate = startLocal.date()

        if eventDate == today or (event.all_day and eventDate == today):
            if getattr(event, "all_day", False):
                timeStr = "All day"
            else:
                timeStr = startLocal.format("HH:mm")
            title = (event.name or "Untitled").strip()
            items.append({"time": timeStr, "title": title})

    # sort by time (all-day first)
    def sortKey(x):
        return (x["time"] != "All day", x["time"])
    items.sort(key=sortKey)
    return items

def buildEmailContext():
    today = timezone.localdate()
    prettyDate = today.strftime("%A, %d %B %Y")
    return {
        "prettyDate": prettyDate,
        "mission": getMission(),
        "quote": getQuoteOfTheDay(),
        "appointments": getTodayAppointments(),
    }
