from PIL import Image, ImageDraw, ImageFont
import cairosvg
import io

WIDTH = 800
HEIGHT = 480

WHITE = "white"
BLACK = "black"

# =========================================
# Canvas
# =========================================

image = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
draw = ImageDraw.Draw(image)

# =========================================
# Fonts
# =========================================

FONT_REGULAR = "assets/fonts/Inter-Regular.ttf"
FONT_BOLD = "assets/fonts/Inter-Bold.ttf"

title_font = ImageFont.truetype(FONT_BOLD, 28)
big_temp_font = ImageFont.truetype(FONT_BOLD, 88)

body_font = ImageFont.truetype(FONT_REGULAR, 22)
small_font = ImageFont.truetype(FONT_REGULAR, 16)
tiny_font = ImageFont.truetype(FONT_REGULAR, 14)

# =========================================
# SVG helper
# =========================================

def load_svg_icon(path, size=(64, 64)):
    png_data = cairosvg.svg2png(
        url=path,
        output_width=size[0],
        output_height=size[1]
    )

    return Image.open(io.BytesIO(png_data)).convert("RGBA")

# =========================================
# Header
# =========================================

draw.text((40, 28), "Trondheim", fill=BLACK, font=title_font)
draw.text((40, 62), "Friday 23 May", fill=BLACK, font=body_font)

draw.text((680, 28), "14°", fill=BLACK, font=title_font)
draw.text((610, 62), "Updated 08:15", fill=BLACK, font=body_font)

draw.line((40, 105, 760, 105), fill=BLACK, width=1)

# =========================================
# Main Weather
# =========================================

main_icon = load_svg_icon(
    "assets/icons/weathericons/weather/svg/partlycloudy_day.svg",
    size=(120, 120)
)

image.paste(main_icon, (40, 135), main_icon)

draw.text((190, 120), "14°", fill=BLACK, font=big_temp_font)

draw.text((200, 255), "Mostly cloudy", fill=BLACK, font=body_font)

draw.text((200, 300), "Feels like 11°", fill=BLACK, font=small_font)
draw.text((200, 326), "Wind 5 m/s NW", fill=BLACK, font=small_font)
draw.text((200, 352), "Rain 0.4 mm", fill=BLACK, font=small_font)

# =========================================
# Forecast Graph
# =========================================

graph_left = 430
graph_top = 175
graph_width = 320
graph_height = 140

# Title
draw.text(
    (430, 120),
    "Next hours",
    fill=BLACK,
    font=body_font
)

hours = ["09", "12", "15", "18", "21", "00", "03"]

temps = [14, 15, 15.5, 14.8, 16.2, 17.5, 16.7]

rain = [0.1, 0.6, 1.1, 0.7, 1.6, 0.8, 0.1]

# =========================================
# Dynamic scaling
# =========================================

temp_min = min(temps)
temp_max = max(temps)

padding = 1.0

scaled_min = temp_min - padding
scaled_max = temp_max + padding

# =========================================
# X positions
# =========================================

x_positions = []

for i in range(len(hours)):

    x = graph_left + int(i * (graph_width / 6))
    x_positions.append(x)

# =========================================
# Top hour labels
# =========================================

for x, hour in zip(x_positions, hours):

    draw.text(
        (x - 12, 145),
        hour,
        fill=BLACK,
        font=small_font
    )

# =========================================
# Grid
# =========================================

horizontal_lines = 4

for i in range(horizontal_lines + 1):

    y = graph_top + int(i * (graph_height / horizontal_lines))

    draw.line(
        (graph_left, y, graph_left + graph_width, y),
        fill=BLACK,
        width=1
    )

# vertical grid
for x in x_positions:

    draw.line(
        (x, graph_top, x, graph_top + graph_height),
        fill=BLACK,
        width=1
    )

# =========================================
# Axis labels
# =========================================

for i in range(horizontal_lines + 1):

    value = scaled_max - (
        (scaled_max - scaled_min)
        * (i / horizontal_lines)
    )

    y = graph_top + int(i * (graph_height / horizontal_lines))

    draw.text(
        (390, y - 8),
        f"{round(value)}°",
        fill=BLACK,
        font=small_font
    )

# =========================================
# Temperature line
# =========================================

line_points = []

for x, temp in zip(x_positions, temps):

    normalized = (
        (temp - scaled_min)
        / (scaled_max - scaled_min)
    )

    y = graph_top + graph_height - int(normalized * graph_height)

    line_points.append((x, y))

draw.line(line_points, fill=BLACK, width=3)

# points
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

# =========================================
# Rain markers
# =========================================

rain_y = 360

draw.text(
    (390, rain_y - 5),
    "Rain",
    fill=BLACK,
    font=tiny_font
)

for x, amount in zip(x_positions, rain):

    intensity = max(1, int(amount * 3))

    for i in range(intensity):

        draw.line(
            (
                x - 6 + (i * 5),
                rain_y,
                x - 3 + (i * 5),
                rain_y
            ),
            fill=BLACK,
            width=2
        )

# =========================================
# Bottom divider
# =========================================

draw.line((40, 390, 760, 390), fill=BLACK, width=1)

# =========================================
# Bottom hourly forecast
# =========================================

forecast_hours = ["09", "12", "15", "18", "21"]

forecast_icons = [
    "clearsky_day",
    "fair_day",
    "rain",
    "rain",
    "cloudy"
]

forecast_temps = ["15°", "17°", "14°", "13°", "11°"]

section_width = 720 // 5

start_x = 40

for i in range(5):

    center_x = start_x + i * section_width + section_width // 2

    # hour
    draw.text(
        (center_x - 14, 402),
        forecast_hours[i],
        fill=BLACK,
        font=small_font
    )

    # icon
    icon = load_svg_icon(
        f"assets/icons/weathericons/weather/svg/{forecast_icons[i]}.svg",
        size=(38, 38)
    )

    image.paste(icon, (center_x - 19, 425), icon)

    # temperature
    draw.text(
        (center_x - 14, 460),
        forecast_temps[i],
        fill=BLACK,
        font=small_font
    )

# =========================================
# Save
# =========================================

image.save("weather_mock.png")

print("Saved weather_mock.png")