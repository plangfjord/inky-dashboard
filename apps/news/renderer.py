# apps/news/renderer.py

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# =========================================================
# COLORS
# =========================================================
BLACK = 0
WHITE = 1

# =========================================================
# FONTS
# =========================================================
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

title_font     = ImageFont.truetype(FONT_BOLD, 36)     # NEWS
headline_font  = ImageFont.truetype(FONT_REGULAR, 17)

# =========================================================
# HELPERS
# =========================================================
def truncate_text(draw, text, font, max_width=518):
    if not text:
        return ""
    
    bbox = draw.textbbox((0, 0), text, font=font)
    if bbox[2] - bbox[0] <= max_width:
        return text

    words = text.split()
    result = ""

    for word in words:
        test = (result + " " + word).strip()
        bbox = draw.textbbox((0, 0), test + "…", font=font)
        if bbox[2] - bbox[0] <= max_width:
            result = test
        else:
            break
    return result.strip() + "…"

# =========================================================
# MAIN
# =========================================================
def render_news_dashboard(cached_news):
    """
    cached_news er en dict med 'curated' og 'all'
    """
    # Hent det kuraterte utvalget vi vil vise
    news_items = cached_news.get("curated", cached_news)

    canvas = Image.new("P", (600, 448), WHITE)
    draw = ImageDraw.Draw(canvas)
    width = 600

    # ====================== HEADER ======================
    draw.text((24, 12), "NEWS", fill=BLACK, font=title_font)

    now = datetime.now()
    draw.text(
        (195, 19),
        f"Last updated: {now.strftime('%A %H:%M')}",
        fill=BLACK,
        font=headline_font
    )

    draw.line((22, 56, width - 22, 56), fill=BLACK, width=3)

    # ====================== SPLIT NEWS ======================
    norwegian_sources = {"NRK", "DN", "TU"}
    
    norwegian_news = [item for item in news_items if item.get("source") in norwegian_sources]
    international_news = [item for item in news_items if item.get("source") not in norwegian_sources]

    y = 78
    spacing = 32

    # --- Norwegian News (6 stk totalt) ---
    for item in norwegian_news[:6]:
        title = truncate_text(draw, item.get("title", ""), headline_font)
        draw.text((26, y), title, fill=BLACK, font=headline_font)
        y += spacing

    # --- Overgang ---
    y += 12

    # --- International News (5 stk) ---
    for item in international_news[:5]:
        title = truncate_text(draw, item.get("title", ""), headline_font)
        draw.text((26, y), title, fill=BLACK, font=headline_font)
        y += spacing

    return canvas