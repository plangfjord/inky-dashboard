from inky.auto import auto
from gpiozero import Button

import time
import traceback

# =========================================================
# APPS IMPORTS
# =========================================================

from apps.weather.data import fetch_weather_data, parse_weather_data
from apps.weather.renderer import render_weather_dashboard

from apps.calendar.data import get_calendar_events
from apps.calendar.renderer import render_calendar_dashboard

from apps.news.data import fetch_news, get_curated_news
from apps.news.renderer import render_news_dashboard

# =========================================================
# DISPLAY & BUTTONS
# =========================================================

display = auto()

button_a = Button(5)
button_b = Button(6)
button_c = Button(16)
button_d = Button(24)

# =========================================================
# APP CONFIG
# =========================================================

apps = ["weather", "calendar", "news"]
current_app_index = 0

# =========================================================
# REFRESH INTERVALS
# =========================================================

WEATHER_REFRESH_INTERVAL = 60 * 30   # 30 min
CALENDAR_REFRESH_INTERVAL = 60 * 5    # 5 min
NEWS_REFRESH_INTERVAL = 60 * 30       # 30 min

# =========================================================
# CACHE
# =========================================================

cached_weather = None
cached_calendar = {"today": [], "tomorrow": []}
cached_news = {}

# =========================================================
# REFRESH FUNCTIONS
# =========================================================

def refresh_weather_data():
    global cached_weather
    print("Fetching weather...")
    raw = fetch_weather_data()
    cached_weather = parse_weather_data(raw)


def refresh_calendar_data():
    global cached_calendar
    print("Fetching calendar...")
    cached_calendar = get_calendar_events()


def refresh_news_data():
    global cached_news
    print("Fetching news...")
    
    all_news = fetch_news()
    curated = get_curated_news(all_news)
    
    cached_news = {
        "curated": curated,
        "all": all_news
    }


# =========================================================
# RENDER FUNCTIONS
# =========================================================

def render_weather():
    return render_weather_dashboard(cached_weather)

def render_calendar():
    return render_calendar_dashboard(
        cached_calendar["today"],
        cached_calendar["tomorrow"]
    )

def render_news():
    return render_news_dashboard(cached_news)

# =========================================================
# APP ROUTER
# =========================================================

def render_current_app():
    current_app = apps[current_app_index]
    print(f"Rendering: {current_app}")

    if current_app == "weather":
        return render_weather()
    elif current_app == "calendar":
        return render_calendar()
    elif current_app == "news":
        return render_news()
    
    return render_weather()


# =========================================================
# DISPLAY
# =========================================================

def refresh_display():
    print("Rendering image...")
    image = render_current_app()

    image = image.resize(display.resolution)
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
refresh_news_data()
refresh_display()

last_weather_refresh = time.time()
last_calendar_refresh = time.time()
last_news_refresh = time.time()


# =========================================================
# MAIN LOOP
# =========================================================

while True:
    try:
        now = time.time()

        # ==================== AUTO REFRESH ====================
        
        if now - last_weather_refresh > WEATHER_REFRESH_INTERVAL:
            print("Refreshing weather...")
            refresh_weather_data()
            if apps[current_app_index] == "weather":
                refresh_display()
            last_weather_refresh = now

        if now - last_calendar_refresh > CALENDAR_REFRESH_INTERVAL:
            print("Refreshing calendar...")
            refresh_calendar_data()
            if apps[current_app_index] == "calendar":
                refresh_display()
            last_calendar_refresh = now

        if now - last_news_refresh > NEWS_REFRESH_INTERVAL:
            print("Refreshing news...")
            refresh_news_data()
            if apps[current_app_index] == "news":
                refresh_display()
            last_news_refresh = now

        # ==================== BUTTONS ====================

        if button_a.is_pressed:
            print("Switch → Weather")
            current_app_index = 0
            refresh_display()
            time.sleep(0.4)

        if button_b.is_pressed:
            print("Switch → Calendar")
            current_app_index = 1
            refresh_calendar_data()
            refresh_display()
            time.sleep(0.4)

        if button_c.is_pressed:
            print("Switch → News + Refresh")
            current_app_index = 2
            refresh_display()
            time.sleep(0.4)

        if button_d.is_pressed:
            print("Manual refresh")
            refresh_display()
            time.sleep(0.4)

        time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        time.sleep(5)