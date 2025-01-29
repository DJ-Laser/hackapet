import pygame
import time
from adafruit_display_text import label
import random

import patch
from blinka_displayio_pygamedisplay import PyGameDisplay
PyGameDisplay._initialize = patch.blinka_pygame_display_initalize_patched
PyGameDisplay._pygame_refresh = patch.blinka_pygame_display_pygamerefresh_patched
import displayio
displayio.Bitmap.__init__ = patch.bitmap_create_init_patched
displayio.TileGrid._fill_area = patch.tilegrid_fill_area_patched
displayio.Palette._get_alpha_palette = patch.palette_make_alpha_palette_patched

display = PyGameDisplay(width=320, height=240)
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
# Must check display.running in the main loop!

while True:
    if display.check_quit():
        break
    display._pygame_refresh()
