from pygame import display, event, image
from pygame.font import Font
from pygame.time import Clock
from kezmenu3 import KezMenu


class Menu(object):
    """Display game options"""

    def __init__(self, screen, position):
        self.running = True
        self.screen = screen
        self.position = position

    def new_game(self):
        """Start a new game"""
        pass

    def exit(self):
        """Exit game"""
        self.running = False

    def fill_background(self):
        """Fill screen with a single image"""
        width = self.screen.get_width()
        height = self.screen.get_height()
        background = image.load('game/res/sprite/background/black.png')

        for y in range(0, height, 240):
            for x in range(0, width, 240):
                self.screen.blit(background, (x, y))

    def draw(self):
        """Draw menu"""
        self.menu = KezMenu(
            ['NEW GAME', self.new_game],
            ['EXIT', self.exit])

        self.menu.position = self.position
        self.menu.color = (205, 205, 205, 100)
        self.menu.focus_color = (255, 255, 255)
        self.menu.font = Font('game/res/font/kenvector_future.ttf', 32)
        self.menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)

        clock = Clock()

        while self.running:
            self.menu.update(event.get(), clock.tick(30) / 1000.)
            self.fill_background()
            self.menu.draw(self.screen)
            display.flip()
