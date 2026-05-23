from inky.inky_uc8159 import Inky

from apps.weather.data import (
    fetch_weather_data,
    parse_weather_data
)

from apps.weather.renderer import (
    render_weather_dashboard
)

# =====================================
# Init display manually
# =====================================

display = Inky(
    resolution=(600, 448),
    colour="multi"
)

display.set_border(display.WHITE)

# =====================================
# Fetch weather
# =====================================

raw = fetch_weather_data()

weather = parse_weather_data(raw)

# =====================================
# Render dashboard
# =====================================

image = render_weather_dashboard(
    weather
)

# =====================================
# Display image
# =====================================

display.set_image(image)

display.show()