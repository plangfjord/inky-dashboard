from PIL import Image, ImageDraw, ImageFont
import cairosvg
import io
from datetime import datetime

from apps.weather.icons import get_weather_text

WIDTH = 800
HEIGHT = 480

WHITE = "white"
BLACK = "black"
BLUE = (0, 90, 255)

FONT_REGULAR = "assets/fonts/Inter-Regular.ttf"
FONT_BOLD = "assets/fonts/Inter-Bold.ttf"


def load_fonts():

    return {
        "title": ImageFont.truetype(FONT_BOLD, 28),
        "big_temp": ImageFont.truetype(FONT_BOLD, 92),
        "body": ImageFont.truetype(FONT_REGULAR, 24),
        "small": ImageFont.truetype(FONT_REGULAR, 16),
        "tiny": ImageFont.truetype(FONT_REGULAR, 13),
    }


def load_svg_icon(path, size=(64, 64)):

    png_data = cairosvg.svg2png(
        url=path,
        output_width=size[0],
        output_height=size[1]
    )

    return Image.open(
        io.BytesIO(png_data)
    ).convert("RGBA")


def get_rain_message(hourly):

    rainy_hours = [
        h for h in hourly
        if h["rain"] > 0
    ]

    if not rainy_hours:
        return None

    max_rain = max(
        h["rain"] for h in rainy_hours
    )

    first_rain = rainy_hours[0]["time"][:2]

    if max_rain < 1:
        return f"Light rain at {first_rain}:00"

    elif max_rain < 3:
        return f"Rain expected at {first_rain}:00"

    else:
        return "Heavy rain later today"


def render_weather_dashboard(weather):

    fonts = load_fonts()

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        WHITE
    )

    draw = ImageDraw.Draw(image)

    # Header

    draw.text(
        (40, 28),
        "Trondheim",
        fill=BLACK,
        font=fonts["title"]
    )

    draw.text(
        (40, 62),
        "Live weather from YR",
        fill=BLACK,
        font=fonts["body"]
    )

    current_time = datetime.now().strftime("%H:%M")

    draw.text(
        (610, 34),
        f"Updated {current_time}",
        fill=BLACK,
        font=fonts["small"]
    )

    draw.line(
        (40, 105, 760, 105),
        fill=BLACK,
        width=1
    )

    # Main weather

    icon_path = (
        "assets/icons/weathericons/weather/svg/"
        f"{weather['symbol_code']}.svg"
    )

    main_icon = load_svg_icon(
        icon_path,
        size=(120, 120)
    )

    image.paste(
        main_icon,
        (40, 180),
        main_icon
    )

    draw.text(
        (185, 120),
        f"{weather['current_temp']}°",
        fill=BLACK,
        font=fonts["big_temp"]
    )

    weather_text = get_weather_text(
        weather["symbol_code"]
    )

    draw.text(
        (200, 225),
        weather_text,
        fill=BLACK,
        font=fonts["body"]
    )

    draw.text(
        (200, 265),
        f"Wind {weather['wind_speed']} m/s",
        fill=BLACK,
        font=fonts["small"]
    )

    draw.text(
        (200, 300),
        f"Humidity {round(weather['humidity'])}%",
        fill=BLACK,
        font=fonts["small"]
    )

    rain_message = get_rain_message(
        weather["hourly"]
    )

    if rain_message:

        draw.text(
            (200, 350),
            rain_message,
            fill=BLUE,
            font=fonts["small"]
        )

    # =====================================
    # Forecast Graph
    # =====================================

    graph_left = 430
    graph_top = 180
    graph_width = 320
    graph_height = 125

    draw.text(
        (430, 120),
        "Next hours",
        fill=BLACK,
        font=fonts["body"]
    )

    hourly = weather["hourly"]

    temps = [h["temp"] for h in hourly]

    temp_min = min(temps)
    temp_max = max(temps)

    actual_range = temp_max - temp_min

    min_visual_range = 4

    visual_range = max(
        actual_range,
        min_visual_range
    )

    center = (temp_max + temp_min) / 2

    scaled_min = center - visual_range / 2
    scaled_max = center + visual_range / 2

    # X positions

    x_positions = []

    for i in range(len(hourly)):

        x = graph_left + int(
            i * (graph_width / 6)
        )

        x_positions.append(x)

    # Vertical grid lines

    for x in x_positions:

        draw.line(
            (
                x,
                graph_top,
                x,
                graph_top + graph_height
            ),
            fill=(220, 220, 220),
            width=1
        )

    # Horizontal temperature grid

    temp_floor = int(scaled_min)
    temp_ceiling = int(scaled_max) + 1

    temp_values = list(
        range(temp_floor, temp_ceiling + 1)
    )

    for temp in temp_values:

        normalized = (
            (temp - scaled_min)
            / (scaled_max - scaled_min)
        )

        y = (
            graph_top
            + graph_height
            - int(normalized * graph_height)
        )

        draw.line(
            (
                graph_left,
                y,
                graph_left + graph_width,
                y
            ),
            fill=(210, 210, 210),
            width=1
        )

        draw.text(
            (390, y - 8),
            f"{temp}°",
            fill=BLACK,
            font=fonts["tiny"]
        )

    # Hour labels

    for x, entry in zip(
        x_positions,
        hourly
    ):

        draw.text(
            (x - 12, 145),
            entry["time"][:2],
            fill=BLACK,
            font=fonts["small"]
        )

    # Temperature line

    line_points = []

    for x, temp in zip(
        x_positions,
        temps
    ):

        normalized = (
            (temp - scaled_min)
            / (scaled_max - scaled_min)
        )

        y = (
            graph_top
            + graph_height
            - int(normalized * graph_height)
        )

        line_points.append((x, y))

    draw.line(
        line_points,
        fill=BLACK,
        width=3
    )

    for point in line_points:

        draw.ellipse(
            (
                point[0] - 4,
                point[1] - 4,
                point[0] + 4,
                point[1] + 4
            ),
            fill=BLACK
        )

    # Rain bars

    has_rain = any(
        h["rain"] > 0
        for h in hourly
    )

    if has_rain:

        rain_base_y = 355
        rain_top_y = 325

        max_rain = max(
            h["rain"]
            for h in hourly
        )

        if max_rain < 1:
            max_rain = 1

        draw.line(
            (
                graph_left + graph_width + 10,
                rain_top_y,
                graph_left + graph_width + 10,
                rain_base_y
            ),
            fill=BLUE,
            width=1
        )

        draw.text(
            (
                graph_left + graph_width + 16,
                rain_top_y - 6
            ),
            f"{round(max_rain,1)}",
            fill=BLUE,
            font=fonts["tiny"]
        )

        draw.text(
            (
                graph_left + graph_width + 16,
                rain_base_y - 10
            ),
            "0",
            fill=BLUE,
            font=fonts["tiny"]
        )

        draw.text(
            (
                graph_left + graph_width + 16,
                rain_base_y + 5
            ),
            "mm",
            fill=BLUE,
            font=fonts["tiny"]
        )

        for x, entry in zip(
            x_positions,
            hourly
        ):

            rain = entry["rain"]

            if rain <= 0:
                continue

            bar_height = int(
                (rain / max_rain)
                * (rain_base_y - rain_top_y)
            )

            draw.rectangle(
                (
                    x - 5,
                    rain_base_y - bar_height,
                    x + 5,
                    rain_base_y
                ),
                fill=BLUE
            )



    # Bottom divider

    draw.line(
        (40, 385, 760, 385),
        fill=BLACK,
        width=1
    )

    # Bottom forecast

    section_width = 720 // 5

    for i, entry in enumerate(weather["hourly"][:5]):

        center_x = (
            40
            + i * section_width
            + section_width // 2
        )

        draw.text(
            (center_x - 14, 398),
            entry["time"][:2],
            fill=BLACK,
            font=fonts["small"]
        )

        icon_path = (
            "assets/icons/weathericons/weather/svg/"
            f"{entry['symbol_code']}.svg"
        )

        icon = load_svg_icon(
            icon_path,
            size=(38, 38)
        )

        image.paste(
            icon,
            (center_x - 19, 420),
            icon
        )

        draw.text(
            (center_x - 14, 455),
            f"{entry['temp']}°",
            fill=BLACK,
            font=fonts["small"]
        )

    return image