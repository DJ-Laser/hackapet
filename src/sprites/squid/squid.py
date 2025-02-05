import math
import random
import displayio

from sprites.base import FloatVelocitySprite, Sprite

from sprites.spike import Spike
from sprites.squid.eye import Eye
from sprites.squid.mouth import Mouth
from sprites.squid.predicted_player import PredictedPlayer

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

  def spawn_spike(self, prediction: PredictedPlayer, dangers) -> bool:
    if self._time_since_last_danger < 10:
      return False
    
    in_air = False

    # find the first moment before the player lands
    while prediction.bottom_extent == prediction.max_y:
      prediction.step(-1)

      if prediction.timesteps == 0:
        # We started on the ground, use the correct number for spikes
        prediction.timesteps = random.randint(5, 7)
        break
    else:
      # in air, step to landing
      prediction.step()
      in_air = True

    offset_x = prediction.offset_x
    if in_air:
      current_height = prediction.max_y - prediction.at(0).bottom_extent

      offset_x *= min(1 / (current_height * prediction.x_velocity) / 30, 1)

    spike_x = int(prediction.center_x + offset_x)
    spike_x = max(8, min(spike_x, 120))

    spike = Spike()
    spike.center_x = spike_x
    spike.y = 96

    dangers.append(spike)
    return True

  def spawn_danger(self, player: FloatVelocitySprite, dangers: displayio.Group):
    lookahead_time = random.randint(5, 10)

    prediction = PredictedPlayer(player)
    prediction.step(lookahead_time)

    if (prediction.bottom_extent >= 110 or prediction.y_velocity > 5) and \
      self.spawn_spike(prediction.copy(), dangers):
      self._time_since_last_danger = 0
  
  def update(self, player: FloatVelocitySprite, spikes: displayio.Group):
    self.track_player(player)
    self.spawn_danger(player, spikes)
    
    self._time_since_last_danger += 1
