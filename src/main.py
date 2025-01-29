import time
import random
from adafruit_display_text import label
import pygame
import displayio

import patch
from blinka_displayio_pygamedisplay import PyGameDisplay
PyGameDisplay._initialize = patch.blinka_pygame_display_initalize_patched
PyGameDisplay.refresh = patch.blinka_pygame_display_pygamerefresh_patched

from sprites.shelly import Shelly

GROUND_BITMAP = displayio.OnDiskBitmap("textures/ground.bmp")
GROUND_SPRITE = displayio.TileGrid(
	GROUND_BITMAP,
	pixel_shader=GROUND_BITMAP.pixel_shader
)

display = PyGameDisplay(width=128, height=128, scale=3)
splash = displayio.Group()
display.show(splash)

player = Shelly()

splash.append(GROUND_SPRITE)
splash.append(player)

while True:    
    player.update(0, False)

    display.refresh()
    if display.check_quit():
        break
