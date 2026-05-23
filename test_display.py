import spidev

from PIL import Image

from inky.inky_uc8159 import Inky


# =====================================
# Open SPI manually first
# =====================================

spi = spidev.SpiDev()

spi.open(0, 0)

spi.max_speed_hz = 488000


# =====================================
# Init display
# =====================================

display = Inky(
    resolution=(600, 448),
    colour="multi"
)

display.set_border(display.WHITE)


# =====================================
# Create image
# =====================================

img = Image.new(
    "P",
    (600, 448),
    display.WHITE
)

display.set_image(img)

display.show()

print("SUCCESS")