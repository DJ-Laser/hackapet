import displayio

from sprites.base import Sprite

SPIKE_BITMAP = displayio.OnDiskBitmap("./textures/spike.bmp")
SPIKE_FRAMEDATA = [1, 4, 2, 2, 4, 2, 4, 1, 1, 1, 20]

class Spike(Sprite):
  def __init__(self, *args, **kwargs):
    self._sprite = displayio.TileGrid(
      SPIKE_BITMAP,
      pixel_shader=SPIKE_BITMAP.pixel_shader,
      tile_width=16,
      tile_height=16,
      default_tile=0,
    )

    super().__init__(self._sprite, *args, **kwargs)

    self._left_hitbox_offset = -2
    self._right_hitbox_offset = self._sprite.tile_width - 2
    self._top_hitbox_offset = -5
    self._bottom_hitbox_offset = self._sprite.tile_height

    self._current_frame = 10
    self._frame_counter = 0
    self._update_sprite()
  
  def _update_sprite(self):
    self._sprite[0] = self._current_frame
    self._frame_counter = 0

    if self._current_frame >= 7:
      self._top_hitbox_offset = -5
    else:
      self._top_hitbox_offset = -7
  
  def is_animation_finished(self):
    return self._current_frame == 10

  def spawn_at(self, x, y):
    self._current_frame = 0
    self._update_sprite()
    self. x = x
    self.y = y

  def animate(self):
    if self._frame_counter >= SPIKE_FRAMEDATA[self._current_frame]:
      self._current_frame = (self._current_frame + 1) % 11
      self._update_sprite()

    if not self.is_animation_finished():
      self._frame_counter += 1

  def is_dangerous(self) -> bool:
    return 5 <= self._current_frame <= 8
  
  def damages_player(self, player) -> bool:
    if not self.is_dangerous():
      return False
    
    return self.collides_with(player)
