from datetime import datetime, timedelta


def get_calendar_events():

    now = datetime.now()

    return [

        {
            "title": "Team Meeting",
            "time": (
                now + timedelta(hours=2)
            ).strftime("%H:%M")
        },

        {
            "title": "Gym",
            "time": (
                now + timedelta(hours=5)
            ).strftime("%H:%M")
        },

        {
            "title": "Dinner",
            "time": (
                now + timedelta(hours=8)
            ).strftime("%H:%M")
        }
    ]