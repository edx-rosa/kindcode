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
    # MVP: dummy data; replace with Google Calendar or your model later
    # Show only items for 'today' to keep it honest & useful
    today = timezone.localdate()
    # Example static list (edit freely)
    return [
        {"time": "07:00", "title": "Workout"},
        {"time": "12:45", "title": "Walk with Chloé"},
        {"time": "17:00", "title": "Zoom with Linda"},
    ]

def buildEmailContext():
    today = timezone.localdate()
    prettyDate = today.strftime("%A, %d %B %Y")
    return {
        "prettyDate": prettyDate,
        "mission": getMission(),
        "quote": getQuoteOfTheDay(),
        "appointments": getTodayAppointments(),
    }
