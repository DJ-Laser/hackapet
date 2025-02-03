import random
import displayio

from sprites.base import FloatVelocitySprite, Sprite, HitboxOffsetSprite

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

    self._time_since_last_danger = -5

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

  def spawn_spike(self, dangers, predicted_x):
    spike = Spike()
    spike.center_x = max(8, min(predicted_x, 120))
    spike.y = 96

    dangers.append(spike)

  def predict_player_position(self, player, lookahead_time) -> tuple[int, int]:
    lookahead_time = 10

    predicted_x = player.center_x + player.x_velocity * lookahead_time
    predicted_y = player.center_y + player.y_velocity * lookahead_time

    predicted_x = max(0, min(predicted_x, 128))
    predicted_y = max(0, min(predicted_y, 128))

    return (int(predicted_x), int(predicted_y))

  def spawn_danger(self, player: FloatVelocitySprite, dangers):
    lookahead_time = random.randint(5, 10)
    if random.random() < 0.2:
      lookahead_time = random.randint(0, 3)

    (predicted_x, predicted_y) = self.predict_player_position(player, lookahead_time)

    if self._time_since_last_danger >= 10 and \
      predicted_y + player.width // 2 >= 106:
      self.spawn_spike(dangers, predicted_x)
      self._time_since_last_danger = 0
  
  def update(self, player: FloatVelocitySprite, spikes: displayio.Group):
    self.track_player(player)
    self.spawn_danger(player, spikes)
    
    self._time_since_last_danger += 1

