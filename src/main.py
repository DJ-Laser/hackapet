import time
import displayio

import patch
from blinka_displayio_pygamedisplay import PyGameDisplay
PyGameDisplay._initialize = patch.blinka_pygame_display_initalize_patched
PyGameDisplay.refresh = patch.blinka_pygame_display_pygamerefresh_patched

from sprites.score import Score
from sprites.base import DangerousSprite, AnimatableSprite
from sprites.shelly import Shelly
from runner.base import Runner
from sprites.squid import Squid

GROUND_BITMAP = displayio.OnDiskBitmap("textures/ground.bmp")

def update_dangers(group, player, score) -> bool:
    for sprite in group:
            if isinstance(sprite, DangerousSprite):
                if sprite.is_dangerous() and sprite.collides_with(player):
                    return True

            if isinstance(sprite, AnimatableSprite):
                sprite.animate()
                if sprite.is_animation_finished():
                    if isinstance(sprite, DangerousSprite):
                        score.increase(sprite.get_score(player))

                    group.remove(sprite)
                    continue
    
    return False

def main(runner: Runner):
    ground = displayio.TileGrid(
        GROUND_BITMAP,
        pixel_shader=GROUND_BITMAP.pixel_shader
    )

    player = Shelly()
    player.center_x = 64
    player.y = 128 - 32

    dangers = displayio.Group()
    squid = Squid()
    
    score_text = Score()

    runner.splash.append(ground)
    runner.splash.append(squid)
    runner.splash.append(player)
    runner.splash.append(dangers)
    runner.splash.append(score_text)

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

        player_hit = update_dangers(dangers, player, score_text)
        if player_hit:
            break

        squid.update(player, dangers)

        player.update(movement_direction, runner.input.middle)

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
