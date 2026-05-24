from datetime import datetime, timedelta
from googleapiclient.discovery import build

from apps.calendar.auth import get_calendar_credentials


def get_calendar_service():
    creds = get_calendar_credentials()
    return build("calendar", "v3", credentials=creds)


def normalize_event(event):
    start_raw = event["start"].get("dateTime", event["start"].get("date"))
    end_raw = event["end"].get("dateTime", event["end"].get("date"))

    all_day = "date" in event["start"]

    if all_day:
        start = datetime.fromisoformat(start_raw)
        end = datetime.fromisoformat(end_raw)
    else:
        start = datetime.fromisoformat(
            start_raw.replace("Z", "+00:00")
        ).astimezone()

        end = datetime.fromisoformat(
            end_raw.replace("Z", "+00:00")
        ).astimezone()

    return {
        "title": event.get("summary", "Untitled"),
        "start": start,
        "end": end,
        "all_day": all_day,
        "location": event.get("location", ""),
    }


def get_events(days=2):
    service = get_calendar_service()

    today_start = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    now = today_start.isoformat() + "Z"
    future = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            timeMax=future,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    items = result.get("items", [])

    return [normalize_event(e) for e in items]


def get_today_events(events):
    today = datetime.now().date()

    return [
        e for e in events
        if e["start"].date() == today
    ]


def get_tomorrow_events(events):
    tomorrow = datetime.now().date() + timedelta(days=1)

    return [
        e for e in events
        if e["start"].date() == tomorrow
    ]


# =========================================================
# DASHBOARD HELPER
# =========================================================

def get_calendar_events():

    events = get_events()

    today_events = get_today_events(
        events
    )

    tomorrow_events = get_tomorrow_events(
        events
    )

    return {
        "today": today_events,
        "tomorrow": tomorrow_events,
    }