from inky.auto import auto
from gpiozero import Button

import time
import traceback

# =========================================================
# WEATHER
# =========================================================

from apps.weather.data import (
    fetch_weather_data,
    parse_weather_data,
)

from apps.weather.renderer import (
    render_weather_dashboard,
)

# =========================================================
# CALENDAR
# =========================================================

from apps.calendar.data import (
    get_calendar_events,
)

from apps.calendar.renderer import (
    render_calendar_dashboard,
)

# =========================================================
# DISPLAY
# =========================================================

display = auto()

# =========================================================
# BUTTONS
# =========================================================

button_a = Button(5)
button_b = Button(6)
button_c = Button(16)
button_d = Button(24)

# =========================================================
# APPS
# =========================================================

apps = [
    "weather",
    "calendar",
]

current_app_index = 0

# =========================================================
# REFRESH
# =========================================================

last_weather_refresh = 0
last_calendar_refresh = 0

WEATHER_REFRESH_INTERVAL = 60 * 30
CALENDAR_REFRESH_INTERVAL = 60 * 5

# =========================================================
# CACHE
# =========================================================

cached_weather = None

cached_calendar = {
    "today": [],
    "tomorrow": [],
}

# =========================================================
# WEATHER
# =========================================================

def refresh_weather_data():

    global cached_weather

    print("Fetching weather...")

    raw = fetch_weather_data()

    cached_weather = parse_weather_data(
        raw
    )

def render_weather():

    return render_weather_dashboard(
        cached_weather
    )

# =========================================================
# CALENDAR
# =========================================================

def refresh_calendar_data():

    global cached_calendar

    print("Fetching calendar...")

    cached_calendar = get_calendar_events()

def render_calendar():

    return render_calendar_dashboard(
        cached_calendar["today"],
        cached_calendar["tomorrow"],
    )

# =========================================================
# APP ROUTER
# =========================================================

def render_current_app():

    current_app = apps[
        current_app_index
    ]

    print(
        f"Rendering: {current_app}"
    )

    if current_app == "weather":

        return render_weather()

    elif current_app == "calendar":

        return render_calendar()

    return render_weather()

# =========================================================
# DISPLAY REFRESH
# =========================================================

def refresh_display():

    print("Rendering image...")

    image = render_current_app()

    image = image.resize(
        display.resolution
    )

    image = image.convert("P")

    image.save("debug.png")

    print("Updating display...")

    display.set_image(image)

    display.show()

    print("Display updated")

# =========================================================
# INITIAL LOAD
# =========================================================

print("Initial data fetch...")

refresh_weather_data()

refresh_calendar_data()

refresh_display()

last_weather_refresh = time.time()
last_calendar_refresh = time.time()

# =========================================================
# MAIN LOOP
# =========================================================

while True:

    try:

        now = time.time()

        # =================================================
        # AUTO REFRESH
        # =================================================

        # =================================================
        # WEATHER REFRESH
        # =================================================

        if (
            now - last_weather_refresh
            > WEATHER_REFRESH_INTERVAL
        ):

            print(
                "Refreshing weather..."
            )

            refresh_weather_data()

            if apps[current_app_index] == "weather":

                refresh_display()

            last_weather_refresh = now

        # =================================================
        # CALENDAR REFRESH
        # =================================================

        if (
            now - last_calendar_refresh
            > CALENDAR_REFRESH_INTERVAL
        ):

            print(
                "Refreshing calendar..."
            )

            refresh_calendar_data()

            if apps[current_app_index] == "calendar":

                refresh_display()

            last_calendar_refresh = now

        # =================================================
        # BUTTON A → WEATHER
        # =================================================

        if button_a.is_pressed:

            print(
                "Weather app"
            )

            current_app_index = 0

            refresh_display()

            time.sleep(0.4)

        # =================================================
        # BUTTON B → CALENDAR
        # =================================================

        if button_b.is_pressed:

            print(
                "Calendar app"
            )

            current_app_index = 1

            refresh_calendar_data()

            refresh_display()

            time.sleep(0.4)

        # =================================================
        # BUTTON C → FORCE REFRESH
        # =================================================

        if button_c.is_pressed:

            print(
                "Refreshing data..."
            )

            refresh_weather_data()

            refresh_calendar_data()

            refresh_display()

            time.sleep(0.5)

        # =================================================
        # BUTTON D → REDRAW
        # =================================================

        if button_d.is_pressed:

            print(
                "Debug refresh"
            )

            refresh_display()

            time.sleep(0.4)

        # =================================================
        # LOOP DELAY
        # =================================================

        time.sleep(0.1)

    except KeyboardInterrupt:

        print("Exiting...")

        break

    except Exception as e:

        print("ERROR:")
        print(e)

        traceback.print_exc()

        time.sleep(5)