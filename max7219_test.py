# coding:utf8

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT
from luma.led_matrix.device import max7219

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=8, height=8, block_orientation=-90)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white")
    # text(draw, (1, 1), "h", fill="white", font=proportional(LCD_FONT))
