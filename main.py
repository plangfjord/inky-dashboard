from inky.auto import auto
from gpiozero import Button

import time
import traceback

#Værstasjon
from apps.weather.data import (
    fetch_weather_data,
    parse_weather_data
)

from apps.weather.renderer import (
    render_weather_dashboard
)

#Kalender
from apps.calendar.data import (
    get_calendar_events
)

from apps.calendar.renderer import (
    render_calendar_dashboard
)

# =====================================
# Display
# =====================================

display = auto()

# =====================================
# Buttons
# =====================================

button_a = Button(5)
button_b = Button(6)
button_c = Button(16)
button_d = Button(24)

# =====================================
# State
# =====================================

apps = [
    "weather",
    "calendar"
]

current_app_index = 0

last_refresh = 0

REFRESH_INTERVAL = 60 * 30

# =====================================
# Weather Render
# =====================================

cached_weather = None


def get_weather():

    global cached_weather

    raw = fetch_weather_data()

    cached_weather = parse_weather_data(raw)


def render_weather():

    return render_weather_dashboard(
        cached_weather
    )


def render_calendar():

    events = get_calendar_events()

    return render_calendar_dashboard(
        events
    )


# =====================================
# App Router
# =====================================

def render_current_app():

    current_app = apps[
        current_app_index
    ]

    if current_app == "weather":

        return render_weather()

    elif current_app == "calendar":

        return render_calendar()

    return render_weather()


# =====================================
# Display Refresh
# =====================================

def refresh_display():

    print("Rendering app...")

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


# =====================================
# Initial Load
# =====================================

print("Fetching initial weather...")

get_weather()

refresh_display()

last_refresh = time.time()

# =====================================
# Main Loop
# =====================================

while True:

    try:

        now = time.time()

        # ==============================
        # Auto refresh every 30 mins
        # ==============================

        if (
            now - last_refresh
            > REFRESH_INTERVAL
        ):

            print(
                "30 minute refresh..."
            )

            get_weather()

            refresh_display()

            last_refresh = now

        # ==============================
        # Button A
        # ==============================

        if button_a.is_pressed:

            print("Button A")

            current_app_index = 0

            refresh_display()

            time.sleep(0.5)

        # ==============================
        # Button B
        # ==============================

        if button_b.is_pressed:

            print("Button B")

            current_app_index = 1

            refresh_display()

            time.sleep(0.5)

        # ==============================
        # Button C
        # ==============================

        if button_c.is_pressed:

            print("Button C")

            current_app_index = 2

            refresh_display()

            time.sleep(0.5)

        # ==============================
        # Button D
        # ==============================

        if button_d.is_pressed:

            print("Button D")

            current_app_index = 3

            refresh_display()

            time.sleep(0.5)

        # Idle sleep

        time.sleep(0.1)

    except KeyboardInterrupt:

        print("Exiting...")

        break

    except Exception as e:

        print(e)

        traceback.print_exc()

        time.sleep(5)