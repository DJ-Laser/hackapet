from adafruit_display_text import label, wrap_text_to_pixels
from adafruit_bitmap_font import bitmap_font

from sprites.base import HitboxOffsetSprite

FONT = bitmap_font.load_font("fonts/munro-10.bdf")

class Dialouge(HitboxOffsetSprite):
  def __init__(self, high_score_mode = False, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._sprite = label.Label(font=FONT, text="", color=0xFFFF00)

    self.append(self._sprite)

    self._text = ""
    self._revealed_chars = 0
    self._reveal_cooldown = 0

    self._update_text()
  
  @property
  def width(self):
    self._sprite.width
  
  @property
  def height(self):
    self._sprite.height

  @property
  def position(self):
    self._sprite.anchored_position
  
  @position.setter
  def position(self, value):
    self._sprite.anchored_position = value
  
  @property
  def anchor(self):
    self._sprite.anchor_point
  
  @anchor.setter
  def anchor(self, value):
    self._sprite.anchor_point = value
  
  @property
  def reveal_finished(self) -> bool:
    return self._revealed_chars == len(self._text)

  def _update_text(self):
    revealed_text = str(self._text[:self._revealed_chars])
    self._sprite.text = "\n".join(wrap_text_to_pixels(revealed_text, 120, FONT))

  def _reset_cooldown(self):
    self._reveal_cooldown = 2

  def update(self):
    if not self.reveal_finished:
      self._reveal_cooldown -= 1
    
    if self._reveal_cooldown == 0:
      self._reset_cooldown()

      revealed_char = self._text[self._revealed_chars]
      if revealed_char == "." or revealed_char == "?" or revealed_char == "!":
        self._reveal_cooldown = 10
      elif revealed_char == ",":
        self._reveal_cooldown = 5

      self._revealed_chars += 1

    self._update_text()

  def set_text(self, text: str):
    self._text = text
    self._revealed_chars = 0
    self._reset_cooldown()
    self._update_text()

  def clear(self):
    self.set_text("")
