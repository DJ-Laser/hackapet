import displayio

from sprites.base import Sprite

SHELLY_BITMAP = displayio.OnDiskBitmap("./textures/shelly.bmp")

class Shelly(Sprite):
  def __init__(self, *args, **kwargs):
    self._sprite = displayio.TileGrid(
      SHELLY_BITMAP,
      pixel_shader=SHELLY_BITMAP.pixel_shader
    )

    self._sprite.flip_x = True
    self.x_velocity = 0
    self.y_velocity = 0
    
    self.min_x = 0
    self.max_x = 128
    self.min_y = 0
    self.max_y = 112

    super().__init__(self._sprite, *args, **kwargs)
  
  def keep_in_bounds(self):
    if self.x < self.min_x:
      self.x = self.min_x
      self.x_velocity = 0

    max_x = self.max_x - self._sprite._pixel_width
    if self.x > max_x:
      self.x = max_x
      self.x_velocity = 0

    if self.y < self.min_y:
      self.y = self.min_y
      self.y_velocity = 0

    max_y = self.max_y - self._sprite._pixel_height
    if self.y > max_y:
      self.y = max_y
      self.y_velocity = 0

  def update(self, direction_input, jump):
    self.y += self.y_velocity
    self.y_velocity += 1

    self.keep_in_bounds()
