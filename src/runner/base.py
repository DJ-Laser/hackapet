from abc import ABCMeta, abstractmethod
import displayio

class Input():
  left: bool = False
  middle: bool = False
  right: bool = False

class Runner(metaclass=ABCMeta):
  input: Input
  splash: displayio.Group
  display: displayio.Display

  def __init__(self):
    self.input = Input()
    self.splash = displayio.Group()

    self.display = self._init_display()
    self.display.show(self.splash)
  
  @abstractmethod
  def _init_display(self):
    return None

  @abstractmethod
  def update():
    pass

  @abstractmethod
  def refresh(self):
    pass

  @abstractmethod
  def check_exit(self) -> bool:
    return False

  def run(self, main_function):
    main_function(self)
