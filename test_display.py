from inky.auto import auto
from PIL import Image, ImageDraw

display = auto()

img = Image.new("P", display.resolution, 1)
draw = ImageDraw.Draw(img)

draw.rectangle((0, 0, 799, 479), fill=2)

display.set_image(img)
display.show()

print("Done")