from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from datetime import datetime
from datetime import timedelta

# =========================================================
# COLORS (RGB FOR SPECTRA)
# =========================================================

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

RED = (220, 0, 0)

GRAY = (140, 140, 140)

LIGHT_GRAY = (220, 220, 220)

VERY_LIGHT_GRAY = (242, 242, 242)

# =========================================================
# FONTS
# =========================================================

FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

header_font = ImageFont.truetype(
    FONT_BOLD,
    32,
)

today_date_font = ImageFont.truetype(
    FONT_REGULAR,
    18,
)

tomorrow_font = ImageFont.truetype(
    FONT_BOLD,
    22,
)

date_font = ImageFont.truetype(
    FONT_REGULAR,
    16,
)

time_font = ImageFont.truetype(
    FONT_REGULAR,
    14,
)

event_font = ImageFont.truetype(
    FONT_BOLD,
    18,
)

tomorrow_event_font = ImageFont.truetype(
    FONT_BOLD,
    15,
)

past_event_font = ImageFont.truetype(
    FONT_REGULAR,
    18,
)

# =========================================================
# HELPERS
# =========================================================

def fit_text_to_width(
    draw,
    text,
    font,
    max_width,
):

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font,
    )

    text_width = bbox[2] - bbox[0]

    if text_width <= max_width:
        return text

    words = text.split(" ")

    fitted = ""

    for word in words:

        test = (
            fitted + " " + word
        ).strip()

        bbox = draw.textbbox(
            (0, 0),
            test + "…",
            font=font,
        )

        test_width = bbox[2] - bbox[0]

        if test_width <= max_width:

            fitted = test

        else:

            fitted += "…"

            break

    return fitted

# =========================================================
# MAIN RENDER
# =========================================================

def render_calendar(
    canvas,
    events_today,
    events_tomorrow,
):

    draw = ImageDraw.Draw(canvas)

    width, height = canvas.size

    # =====================================================
    # AUTO RANGE
    # =====================================================

    if not events_today and not events_tomorrow:

        START_HOUR = 8
        END_HOUR = 18

    else:

        all_hours = []

        for event in (
            events_today +
            events_tomorrow
        ):

            start = event["start"]
            end = event["end"]

            start_decimal = (
                start.hour +
                (start.minute / 60)
            )

            end_decimal = (
                end.hour +
                (end.minute / 60)
            )

            all_hours.append(
                start_decimal
            )

            all_hours.append(
                end_decimal
            )

        START_HOUR = max(
            6,
            int(min(all_hours)) - 1
        )

        END_HOUR = min(
            23,
            int(max(all_hours)) + 2
        )

    # =====================================================
    # LAYOUT
    # =====================================================

    LEFT_WIDTH = int(width * 0.68)

    HEADER_HEIGHT = 88

    TIMELINE_TOP = HEADER_HEIGHT
    TIMELINE_BOTTOM = height - 18

    HOUR_COUNT = END_HOUR - START_HOUR

    HOUR_HEIGHT = (
        TIMELINE_BOTTOM - TIMELINE_TOP
    ) / HOUR_COUNT

    # =====================================================
    # BACKGROUND
    # =====================================================

    draw.rectangle(
        (
            0,
            0,
            width,
            height,
        ),
        fill=WHITE,
    )

    # =====================================================
    # HEADER
    # =====================================================

    today = datetime.now()

    tomorrow = (
        today +
        timedelta(days=1)
    )

    draw.text(
        (18, 10),
        "TODAY",
        fill=BLACK,
        font=header_font,
    )

    draw.text(
        (178, 22),
        today.strftime("%A %d %b"),
        fill=GRAY,
        font=today_date_font,
    )

    draw.text(
        (LEFT_WIDTH + 16, 16),
        "TOMORROW",
        fill=BLACK,
        font=tomorrow_font,
    )

    draw.text(
        (LEFT_WIDTH + 16, 46),
        tomorrow.strftime("%A %d %b"),
        fill=GRAY,
        font=date_font,
    )

    # =====================================================
    # DIVIDERS
    # =====================================================

    draw.line(
        (
            0,
            HEADER_HEIGHT,
            width,
            HEADER_HEIGHT,
        ),
        fill=LIGHT_GRAY,
        width=1,
    )

    draw.line(
        (
            LEFT_WIDTH,
            10,
            LEFT_WIDTH,
            height - 10,
        ),
        fill=LIGHT_GRAY,
        width=1,
    )

    # =====================================================
    # TIMELINE
    # =====================================================

    for hour in range(
        START_HOUR,
        END_HOUR + 1,
    ):

        y = int(
            TIMELINE_TOP +
            (
                (hour - START_HOUR)
                * HOUR_HEIGHT
            )
        )

        # HOUR LINE

        draw.line(
            (
                60,
                y,
                width,
                y,
            ),
            fill=LIGHT_GRAY,
            width=1,
        )

        # HALF HOUR LINE

        half_y = int(
            y + (HOUR_HEIGHT / 2)
        )

        draw.line(
            (
                60,
                half_y,
                width,
                half_y,
            ),
            fill=VERY_LIGHT_GRAY,
            width=1,
        )

        # TIME LABEL BG

        draw.rectangle(
            (
                0,
                y - 9,
                46,
                y + 9,
            ),
            fill=WHITE,
        )

        draw.text(
            (
                8,
                y - 7,
            ),
            f"{hour:02d}",
            fill=GRAY,
            font=time_font,
        )

    # =====================================================
    # CURRENT TIME LINE
    # =====================================================

    now = datetime.now()

    current_decimal = (
        now.hour +
        (now.minute / 60)
    )

    if START_HOUR <= current_decimal <= END_HOUR:

        now_y = int(
            TIMELINE_TOP +
            (
                (current_decimal - START_HOUR)
                * HOUR_HEIGHT
            )
        )

        draw.line(
            (
                60,
                now_y,
                LEFT_WIDTH - 18,
                now_y,
            ),
            fill=RED,
            width=3,
        )

        draw.ellipse(
            (
                54,
                now_y - 6,
                66,
                now_y + 6,
            ),
            fill=RED,
        )

    # =====================================================
    # EVENT DRAWER
    # =====================================================

    def draw_event(
        event,
        x,
        card_width,
        compact=False,
    ):

        start = event["start"]
        end = event["end"]

        duration_hours = (
            end - start
        ).seconds / 3600

        start_decimal = (
            start.hour +
            (start.minute / 60)
        )

        y = int(
            TIMELINE_TOP +
            (
                (start_decimal - START_HOUR)
                * HOUR_HEIGHT
            )
        )

        event_height = int(
            duration_hours * HOUR_HEIGHT
        )

        event_height = max(
            event_height,
            56,
        )

        now = datetime.now(
            start.tzinfo
        )

        is_current = (
            start <= now <= end
        )

        is_past = end < now

        # =================================================
        # STYLING
        # =================================================

        background = VERY_LIGHT_GRAY
        outline = LIGHT_GRAY
        text_fill = BLACK
        accent = BLACK

        font = (
            tomorrow_event_font
            if compact
            else event_font
        )

        if is_current:

            background = RED
            outline = RED
            text_fill = WHITE
            accent = WHITE

        elif is_past:

            background = WHITE
            outline = LIGHT_GRAY
            text_fill = GRAY
            accent = GRAY

            font = past_event_font

        # =================================================
        # CARD
        # =================================================

        draw.rounded_rectangle(
            (
                x,
                y,
                x + card_width,
                y + event_height,
            ),
            radius=12,
            fill=background,
            outline=outline,
            width=1,
        )

        # =================================================
        # ACCENT LINE
        # =================================================

        draw.line(
            (
                x + 10,
                y + 8,
                x + 10,
                y + event_height - 8,
            ),
            fill=accent,
            width=4,
        )

        # =================================================
        # TITLE
        # =================================================

        title = fit_text_to_width(
            draw=draw,
            text=event["title"],
            font=font,
            max_width=card_width - 34,
        )

        draw.text(
            (
                x + 24,
                y + 8,
            ),
            title,
            fill=text_fill,
            font=font,
        )

        # =================================================
        # TIME
        # =================================================

        time_text = (
            f"{start.strftime('%H:%M')} → "
            f"{end.strftime('%H:%M')}"
        )

        draw.text(
            (
                x + 24,
                y + 30,
            ),
            time_text,
            fill=text_fill,
            font=time_font,
        )

    # =====================================================
    # TODAY
    # =====================================================

    for event in events_today:

        draw_event(
            event=event,
            x=74,
            card_width=LEFT_WIDTH - 110,
        )

    # =====================================================
    # TOMORROW
    # =====================================================

    for event in events_tomorrow:

        draw_event(
            event=event,
            x=LEFT_WIDTH + 10,
            card_width=width - LEFT_WIDTH - 18,
            compact=True,
        )

    return canvas

# =========================================================
# DASHBOARD WRAPPER
# =========================================================

def render_calendar_dashboard(
    events_today,
    events_tomorrow,
):

    canvas = Image.new(
        "RGB",
        (600, 448),
        WHITE,
    )

    return render_calendar(
        canvas,
        events_today,
        events_tomorrow,
    )

# =========================================================
# ALIAS
# =========================================================

def draw_calendar(
    canvas,
    events_today,
    events_tomorrow,
):

    return render_calendar(
        canvas,
        events_today,
        events_tomorrow,
    )