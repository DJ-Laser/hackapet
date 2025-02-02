from abc import ABCMeta, abstractmethod
from typing import Self, Protocol, runtime_checkable

import displayio

class Sprite(displayio.Group, metaclass=ABCMeta):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @property
  @abstractmethod
  def width(self) -> int:
    pass

  @property
  @abstractmethod
  def height(self) -> int:
    pass
  
  @property
  def center_x(self) -> int:
    return self.x + self.width // 2

  @center_x.setter
  def center_x(self, value):
    self.x = value - self.width // 2

  @property
  def center_y(self) -> int:
    return self.y + self.height // 2

  @center_y.setter
  def center_y(self, value):
    self.y = value - self.height // 2

  @property
  @abstractmethod
  def left_extent(self) -> int:
    pass

  @property
  @abstractmethod
  def right_extent(self) -> int:
    pass
  
  @property
  @abstractmethod
  def top_extent(self) -> int:
    pass

  @property
  @abstractmethod
  def bottom_extent(self) -> int:
    pass

  @property
  def hitbox_width(self):
    return self.right_extent - self.left_extent
  
  @property
  def hitbox_height(self):
    return self.bottom_extent - self.top_extent

  def collides_with(self, other: Self) -> bool:
    return \
    self.left_extent < other.right_extent and \
    self.right_extent > other.left_extent and \
    self.top_extent < other.bottom_extent and \
    self.bottom_extent > other.top_extent

class HitboxOffsetSprite(Sprite, metaclass=ABCMeta):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @property
  def _left_hitbox_offset(self) -> int:
    return 0

  @property
  def _right_hitbox_offset(self) -> int:
    return 0

  @property
  def _top_hitbox_offset(self) -> int:
    return 0

  @property
  def _bottom_hitbox_offset(self) -> int:
    return 0

  @property
  def left_extent(self) -> int:
    return self.x - self._left_hitbox_offset

  @property
  def right_extent(self) -> int:
    return self.x + self.width + self._right_hitbox_offset
  
  @property
  def top_extent(self) -> int:
    return self.y - self._top_hitbox_offset

  @property
  def bottom_extent(self) -> int:
    return self.y + self.height + self._bottom_hitbox_offset

@runtime_checkable
class DangerousSprite(Protocol):
  @abstractmethod
  def is_dangerous(self) -> bool:
    return False

@runtime_checkable
class AnimatableSprite(Protocol):
  @abstractmethod
  def animate(self):
    pass

  @abstractmethod
  def is_animation_finished() -> bool:
    return False
