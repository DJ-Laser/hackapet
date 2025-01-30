import displayio

from sprites.base import Sprite

SPIKE_BITMAP = displayio.OnDiskBitmap("./textures/spike.bmp")
SPIKE_FRAMEDATA = [1, 4, 1, 1, 4, 2, 4, 1, 1, 1, 20]

class Spike(Sprite):
  def __init__(self, *args, **kwargs):
    self._sprite = displayio.TileGrid(
      SPIKE_BITMAP,
      pixel_shader=SPIKE_BITMAP.pixel_shader,
      tile_width=16,
      tile_height=16,
      default_tile=0,
      x=(128 - 16) // 2,
      y=96
    )

    super().__init__(self._sprite, *args, **kwargs)
    self._current_frame = 0
    self._frame_counter = 0
  
  def animate(self):
    self._frame_counter += 1

    if self._frame_counter >= SPIKE_FRAMEDATA[self._current_frame]:
      self._current_frame = (self._current_frame + 1) % 11
      self._sprite[0] = self._current_frame
      self._frame_counter = 0
    
