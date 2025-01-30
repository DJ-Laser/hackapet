import time
import random
import displayio

from sprites.shelly import Shelly
from runner.base import Runner

GROUND_BITMAP = displayio.OnDiskBitmap("textures/ground.bmp")

def main(runner: Runner):
    ground = displayio.TileGrid(
        GROUND_BITMAP,
        pixel_shader=GROUND_BITMAP.pixel_shader
    )

    player = Shelly()

    runner.splash.append(ground)
    runner.splash.append(player)

    while True:
        runner.update()
        player.update(0, False)

        runner.refresh()
        if runner.check_exit():
            break

if __name__ == "__main__":
    from runner.pygame import PygameRunner
    runner = PygameRunner()
    runner.run(main)
