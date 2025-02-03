import random
import displayio

from sprites.base import Sprite, HitboxOffsetSprite

import patch
from sprites.spike import Spike
displayio.Bitmap.__init__ = patch.bitmap_create_init_patched

BRACKET_BITMAP = displayio.OnDiskBitmap("./textures/squid_parts/bracket.bmp")
MOUTH_BITMAP = displayio.OnDiskBitmap("./textures/squid_parts/mouth.bmp")
EYE_BITMAP = displayio.OnDiskBitmap("./textures/squid_parts/eye.bmp")

class Mouth(HitboxOffsetSprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = displayio.TileGrid(
      MOUTH_BITMAP,
      pixel_shader=MOUTH_BITMAP.pixel_shader
    )

    self.append(self._sprite)

  @property
  def width(self):
    return self._sprite.tile_width

  @property
  def height(self):
    return self._sprite.tile_height

class Eye(HitboxOffsetSprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._top_bracket = displayio.TileGrid(
      BRACKET_BITMAP,
      pixel_shader=BRACKET_BITMAP.pixel_shader,
    )

    self._eye = displayio.TileGrid(
      EYE_BITMAP,
      pixel_shader=EYE_BITMAP.pixel_shader,
    )

    self._bottom_bracket = displayio.TileGrid(
      BRACKET_BITMAP,
      pixel_shader=BRACKET_BITMAP.pixel_shader,
    )
    
    self._bottom_bracket.flip_y = True

    self.height = 30
    self.eye_x = 0
    self.eye_y = 0
    
    self.append(self._top_bracket)
    self.append(self._eye)
    self.append(self._bottom_bracket)
  
  @property
  def width(self):
    return self._top_bracket.tile_width

  @property
  def height(self):
    return self._bottom_bracket.y + self._bottom_bracket.tile_height

  @height.setter
  def height(self, value):
    self._bottom_bracket.y = value - self._bottom_bracket.tile_height
  
  @property
  def eye_x(self):
    return self._eye.x - self.width // 2 + self._eye.tile_width // 2
  
  @eye_x.setter
  def eye_x(self, value):
    self._eye.x = value + self.width // 2 - self._eye.tile_width // 2
  
  @property
  def eye_y(self):
    return self._eye.y - self.height // 2 + self._eye.tile_height // 2
  
  @eye_y.setter
  def eye_y(self, value):
    self._eye.y = value + self.width // 2 - self._eye.tile_height // 2

class Squid(Sprite):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._left_eye = Eye()
    self._left_eye.center_x = 39
    self._left_eye.center_y = 25

    self._right_eye = Eye()
    self._right_eye.center_x = 128 - 39
    self._right_eye.center_y = 25

    self._mouth = Mouth()
    self._mouth.center_x = 64
    self._mouth.center_y = 57

    self.append(self._left_eye)
    self.append(self._right_eye)
    self.append(self._mouth)

    self._spike_spawn_cooldown = 30

  @property
  def width(self):
    return self.hitbox_width

  @property
  def height(self):
    return self.hitbox_height
  
  @property
  def left_extent(self):
    return min(self._left_eye.left_extent, self._right_eye.left_extent)

  @property
  def right_extent(self):
    return max(self._left_eye.right_extent, self._right_eye.right_extent)
  
  @property
  def top_extent(self):
    return min(self._left_eye.top_extent, self._right_eye.top_extent)

  @property
  def bottom_extent(self):
    return max(self._left_eye.bottom_extent, self._right_eye.bottom_extent)

  def track_player(self, player: Sprite):
    x_dist = (player.center_x - self.center_x)
    y_dist = (player.center_y - self.center_y)

    eye_x = x_dist // 10
    eye_y = y_dist // 19

    self._left_eye.eye_x = eye_x
    self._left_eye.eye_y = eye_y

    self._right_eye.eye_x = eye_x
    self._right_eye.eye_y = eye_y

  def spawn_spike(self, player, spikes):
    spikes.append(Spike(random.randint(0, 128 - 16), 96))
    self._spike_spawn_cooldown = 15

  def update(self, player: Sprite, spikes: displayio.Group):
    self.track_player(player)


    if self._spike_spawn_cooldown <= 0:
      self.spawn_spike(player, spikes)
      
    self._spike_spawn_cooldown -= 1
