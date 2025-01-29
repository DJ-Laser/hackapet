import displayio

class Sprite(displayio.Group):
  def __init__(self, sprite, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.append(sprite)
