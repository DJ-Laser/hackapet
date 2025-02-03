from typing import Self
import displayio

from sprites.base import HitboxOffsetSprite

SHELLY_BITMAP = displayio.OnDiskBitmap("./textures/shelly.bmp")

class Shelly(HitboxOffsetSprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = displayio.TileGrid(
      SHELLY_BITMAP,
      pixel_shader=SHELLY_BITMAP.pixel_shader
    )

    self._sprite.flip_x = True
    self.append(self._sprite)

    self._float_x = 0
    self._float_y = 0
    self.x_velocity = 0
    self.y_velocity = 0
    
    self.min_x = 0
    self.max_x = 128
    self.min_y = -5
    self.max_y = 112

    self.grounded = False

    self.max_air_jumps = 1
    self.remaining_air_jumps = self.max_air_jumps
    self.jump_held = False

  @property
  def float_x(self) -> float:
    return self._float_x
  
  @float_x.setter
  def float_x(self, value):
    super(Shelly, type(self)).x.__set__(self, int(value))
    self._float_x = value

  @property
  def x(self) -> int:
    return int(self.float_x)
  
  @x.setter
  def x(self, value):
    self.float_x = value  

  @property
  def float_y(self) -> float:
    return self._float_y
  
  @float_y.setter
  def float_y(self, value):
    super(Shelly, type(self)).y.__set__(self, int(value))
    self._float_y = value
  
  @property
  def y(self) -> int:
    return int(self.float_y)
  
  @y.setter
  def y(self, value: float):
    self.float_y = value
  
  @property
  def _left_hitbox_offset(self):
    return -1

  @property
  def _right_hitbox_offset(self):
    return -1
  
  @property
  def _top_hitbox_offset(self):
    return -6
  
  @property
  def width(self):
    return self._sprite.tile_width

  @property
  def height(self):
    return self._sprite.tile_height
  
  def keep_in_bounds(self):
    if self.float_x < self.min_x:
      self.x = self.min_x
      self.x_velocity = 0

    max_x = self.max_x - self._sprite.tile_width
    if self.float_x > max_x:
      self.x = max_x
      self.x_velocity = 0

    if self.float_y < self.min_y:
      self.y = self.min_y
      self.y_velocity = 0

    max_y = self.max_y - self._sprite.tile_height
    if self.float_y > max_y:
      self.y = max_y
      self.y_velocity = 0
  
  def clamp_x_velocity(self, limit):
    self.x_velocity = max(-limit, min(self.x_velocity, limit))

  def clamp_y_velocity(self, limit):
    self.y_velocity = max(-limit, min(self.y_velocity, limit))

  def check_grounded(self):
    self.grounded = self.float_y >= self.max_y - self._sprite._pixel_height
    
    if self.grounded:
      self.remaining_air_jumps = self.max_air_jumps

  def jump(self):
    if self.jump_held:
      return

    if self.grounded:
      self.y_velocity = min(-8.1, self.y_velocity)
    elif self.remaining_air_jumps > 0:
      self.remaining_air_jumps -= 1
      self.y_velocity = min(-6.9, self.y_velocity)
    else:
      return
    
    self.jump_held = True
    
  def update(self, movement_direction, jump):
    if (not (jump and self.jump_held)) and self.y_velocity < 0:
      self.y_velocity += 1.4
    else:
      self.y_velocity += 1
    
    self.check_grounded()
    if jump:
      self.jump()
    else:
      self.jump_held = False

    self.clamp_y_velocity(10)
    self.float_y += self.y_velocity

    self.x_velocity = self.x_velocity + movement_direction * 1.5
    if movement_direction > 0:
      self._sprite.flip_x = True
    elif movement_direction < 0:
      self._sprite.flip_x = False
    else:
      self.x_velocity *= 0.80
    
    self.clamp_x_velocity(3)
    self.float_x += self.x_velocity

    self.keep_in_bounds()