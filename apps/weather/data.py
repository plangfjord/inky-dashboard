import requests 
from datetime import datetime

URL = (
    "https://api.met.no/weatherapi/locationforecast/2.0/compact"
)

HEADERS = {
    "User-Agent": "inky-dashboard/1.0 github.com/peder"
}

LATITUDE = 63.4305
LONGITUDE = 10.3951


def fetch_weather_data():

    response = requests.get(
        URL,
        headers=HEADERS,
        params={
            "lat": LATITUDE,
            "lon": LONGITUDE
        }
    )

    response.raise_for_status()

    return response.json()


def parse_weather_data(data):

    timeseries = data["properties"]["timeseries"]

    current = timeseries[0]

    current_details = current["data"]["instant"]["details"]

    current_summary = current["data"]["next_1_hours"]["summary"]

    weather = {
        "current_temp": round(
            current_details["air_temperature"]
        ),

        "wind_speed": round(
            current_details["wind_speed"],
            1
        ),

        "humidity": current_details["relative_humidity"],

        "symbol_code": current_summary["symbol_code"],

        "hourly": []
    }

    # =====================================
    # Smart forecast start logic
    # =====================================

    now = datetime.now()

    current_hour = now.hour

    # After xx:45:
    # move to next hour

    if now.minute >= 45:

        current_hour = (
            current_hour + 1
        ) % 24

    future_entries = []

    started = False

    for entry in timeseries:

        entry_time = datetime.fromisoformat(
            entry["time"].replace("Z", "+00:00")
        )

        local_time = (
            entry_time
            .astimezone()
            .replace(tzinfo=None)
        )

        entry_hour = local_time.hour

        # Start collecting
        # when we hit target hour

        if not started:

            if entry_hour == current_hour:

                started = True

            else:

                continue

        future_entries.append(entry)

    # =====================================
    # Build hourly forecast
    # =====================================

    for entry in future_entries[:7]:

        details = entry["data"]["instant"]["details"]

        forecast = entry["data"].get("next_1_hours")

        rain_amount = 0

        symbol_code = "cloudy"

        if forecast:

            rain_amount = (
                forecast["details"]
                .get("precipitation_amount", 0)
            )

            symbol_code = (
                forecast["summary"]["symbol_code"]
            )

        local_time = datetime.fromisoformat(
            entry["time"].replace("Z", "+00:00")
        ).astimezone()

        weather["hourly"].append({

            "time": local_time.strftime("%H:%M"),

            "temp": round(
                details["air_temperature"]
            ),

            "rain": round(rain_amount, 1),

            "symbol_code": symbol_code
        })

    return weather


if __name__ == "__main__":

    raw = fetch_weather_data()

    weather = parse_weather_data(raw)

    pprint(weather)