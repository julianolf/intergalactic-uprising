from pygame import init, display
from .menu import Menu


class Game(object):
    """Intergalactic Uprise Game"""

    _screen_size = (768, 512)
    _menu_pos = ((_screen_size[0]/2-100), (_screen_size[1]/2-50))

    def start(self):
        # Initialize pygame modules
        init()

        # Initialize and display main menu
        self.screen = display.set_mode(self._screen_size)
        self.main_menu = Menu(self.screen, self._menu_pos)
        self.main_menu.draw()
