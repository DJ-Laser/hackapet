import time
import random
import displayio

from sprites.shelly import Shelly
from runner.base import Runner
from sprites.spike import Spike

GROUND_BITMAP = displayio.OnDiskBitmap("textures/ground.bmp")

def main(runner: Runner):
    ground = displayio.TileGrid(
        GROUND_BITMAP,
        pixel_shader=GROUND_BITMAP.pixel_shader
    )

    player = Shelly()
    spike = Spike()

    runner.splash.append(ground)
    runner.splash.append(player)
    runner.splash.append(spike)

    target_fps = 30
    target_execution_time = 1.0 / target_fps
    while True:
        start_time = time.perf_counter()
        runner.update()

        movement_direction = 0
        if runner.input.left:
            movement_direction -= 1
        
        if runner.input.right:
            movement_direction += 1
        
        player.update(movement_direction, runner.input.middle)
        spike.animate()
        print(spike.damages_player(player))

        runner.refresh()
        if runner.check_exit():
            break
        
        end_time = time.perf_counter()
        process_time = end_time - start_time
        sleep_time = target_execution_time - process_time

        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    from runner.pygame import PygameRunner
    runner = PygameRunner()
    runner.run(main)
