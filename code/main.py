
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

pygame.init()

display = PyGameDisplay(width=320, height=240, hw_accel=False)
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

"""
pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forest_background = displayio.OnDiskBitmap("forestbackground.bmp")
bg_sprite = displayio.TileGrid(forest_background, pixel_shader=forest_background.pixel_shader)
splash.append(bg_sprite)

cat_sheet = displayio.OnDiskBitmap("cat-Sheet.bmp")

tile_width = 32
tile_height = 32

cat_sprite = displayio.TileGrid(
    cat_sheet,
    pixel_shader=cat_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=(display.width - tile_width) // 2,  
    y=display.height - tile_height - 10     
)

splash.append(cat_sprite)

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")

fireballs = []

def spawn_fireball():
    x_position = random.randint(0, display.width - fireball_bitmap.width)
    fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fireball_bitmap.width,
        tile_height=fireball_bitmap.height,
        x=x_position,
        y=-32
    )
    fireballs.append(fireball)
    splash.append(fireball)

# Function to check for collisions
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 32 and
        sprite1.x + 32 > sprite2.x and
        sprite1.y < sprite2.y + 32 and
        sprite1.y + 32 > sprite2.y
    )

death = displayio.OnDiskBitmap("restart.bmp")

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader=cat_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=64,
        tile_height=32,
        default_tile=0,
        x=(display.width - 64) // 2,  
        y=(display.height - 32) // 2  
    )
    splash.append(death_hi)
    for i in fireballs:
        splash.remove(i)
    fireballs.clear()

frame = 0
speed = 4 
game_over = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True:
                for i in fireballs:
                    splash.remove(i)
                fireballs.clear()
                splash.remove(death_hi)
                game_over = False


    keys = pygame.key.get_pressed()

    if game_over == False:
        if keys[pygame.K_LEFT]:
            cat_sprite.x -= speed
            print("LEF")
        if keys[pygame.K_RIGHT]:
            cat_sprite.x += speed
            print("RIG")
        if random.random() < 0.05:  # spawn rate
            spawn_fireball()

    for fireball in fireballs:
        fireball.y += 5 
        if fireball.y > display.height:
            splash.remove(fireball)
            fireballs.remove(fireball)
        elif check_collision(cat_sprite, fireball):
            print("DIE")
            game_over = True
            display_game_over()

    cat_sprite[0] = frame
    frame = (frame + 1) % (cat_sheet.width // tile_width)

    time.sleep(0.1)
"""