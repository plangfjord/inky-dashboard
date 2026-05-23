SYMBOL_TEXT = {

    "clearsky_day": "Clear sky",
    "clearsky_night": "Clear night",

    "fair_day": "Fair",
    "fair_night": "Fair",

    "partlycloudy_day": "Mostly cloudy",
    "partlycloudy_night": "Mostly cloudy",

    "cloudy": "Cloudy",

    "rain": "Rain",

    "lightrain": "Light rain",

    "heavyrain": "Heavy rain",

    "fog": "Fog",

    "snow": "Snow",
}


def get_weather_text(symbol_code):

    clean_code = symbol_code.split("_")[0]

    return SYMBOL_TEXT.get(
        clean_code,
        clean_code.replace("_", " ").title()
    )