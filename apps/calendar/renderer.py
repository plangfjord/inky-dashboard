from PIL import (
    Image,
    ImageDraw,
    ImageFont
)

from datetime import datetime

WIDTH = 800
HEIGHT = 480

FONT_REGULAR = (
    "assets/fonts/Inter-Regular.ttf"
)

FONT_BOLD = (
    "assets/fonts/Inter-Bold.ttf"
)

BLACK = 0
WHITE = 1
BLUE = 2


def load_fonts():

    return {

        "title": ImageFont.truetype(
            FONT_BOLD,
            36
        ),

        "date": ImageFont.truetype(
            FONT_BOLD,
            64
        ),

        "body": ImageFont.truetype(
            FONT_REGULAR,
            24
        ),

        "small": ImageFont.truetype(
            FONT_REGULAR,
            18
        ),
    }


def render_calendar_dashboard(events):

    fonts = load_fonts()

    image = Image.new(
        "P",
        (WIDTH, HEIGHT),
        WHITE
    )

    draw = ImageDraw.Draw(image)

    # =====================================
    # Header
    # =====================================

    draw.text(
        (40, 30),
        "Calendar",
        fill=BLACK,
        font=fonts["title"]
    )

    draw.line(
        (40, 90, 760, 90),
        fill=BLACK,
        width=2
    )

    # =====================================
    # Date
    # =====================================

    now = datetime.now()

    day = now.strftime("%A")

    date = now.strftime("%d %B")

    draw.text(
        (40, 120),
        day,
        fill=BLUE,
        font=fonts["body"]
    )

    draw.text(
        (40, 160),
        date,
        fill=BLACK,
        font=fonts["date"]
    )

    # =====================================
    # Events
    # =====================================

    draw.text(
        (420, 120),
        "Upcoming",
        fill=BLACK,
        font=fonts["body"]
    )

    y = 180

    for event in events:

        draw.rounded_rectangle(
            (
                420,
                y,
                740,
                y + 70
            ),
            radius=10,
            outline=BLACK,
            width=2
        )

        draw.text(
            (440, y + 14),
            event["title"],
            fill=BLACK,
            font=fonts["body"]
        )

        draw.text(
            (440, y + 40),
            event["time"],
            fill=BLUE,
            font=fonts["small"]
        )

        y += 90

    return image