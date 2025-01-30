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

    super().__init__(self._sprite, *args, **kwargs)

    self._left_hitbox_offset = -1
    self._right_hitbox_offset = self._sprite.tile_width - 1
    self._top_hitbox_offset = -6
    self._bottom_hitbox_offset = self._sprite.tile_height

    self.float_x = float(self.x)
    self.float_y = float(self.y)
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
  
  def keep_in_bounds(self):
    if self.float_x < self.min_x:
      self.float_x = self.min_x
      self.x_velocity = 0

    max_x = self.max_x - self._sprite.tile_width
    if self.float_x > max_x:
      self.float_x = max_x
      self.x_velocity = 0

    if self.float_y < self.min_y:
      self.float_y = self.min_y
      self.y_velocity = 0

    max_y = self.max_y - self._sprite.tile_height
    if self.float_y > max_y:
      self.float_y = max_y
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
    self.x = int(self.float_x)
    self.y = int(self.float_y)
