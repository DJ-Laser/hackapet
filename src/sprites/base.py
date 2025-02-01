from abc import ABCMeta
from typing import Self

import displayio

class Sprite(displayio.Group, metaclass=ABCMeta):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._left_hitbox_offset = 0
    self._right_hitbox_offset = 0
    self._top_hitbox_offset = 0
    self._bottom_hitbox_offset = 0

  @property
  def left_extent(self) -> int:
    return self.x - self._left_hitbox_offset

  @property
  def right_extent(self) -> int:
    return self.x + self._right_hitbox_offset
  
  @property
  def top_extent(self) -> int:
    return self.y - self._top_hitbox_offset

  @property
  def bottom_extent(self) -> int:
    return self.y + self._bottom_hitbox_offset

  def collides_with(self, other: Self) -> bool:
    return \
    self.left_extent < other.right_extent and \
    self.right_extent > other.left_extent and \
    self.top_extent < other.bottom_extent and \
    self.bottom_extent > other.top_extent
