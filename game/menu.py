import pygame
from game import settings
from kezmenu3 import KezMenu


class Menu(object):
    """Display game options."""

    def __init__(self, game):
        """Initializes the menu.

        Args:
            game: The running game instance.
        """
        self.game = game
        self.running = False
        self.clock = pygame.time.Clock()

    def new_game(self):
        """Starts a new game."""
        self.running = False
        self.game.new()

    def exit(self):
        """Exit game."""
        self.running = False

    def fill_background(self):
        """Fill screen with a single image."""
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        background = pygame.image.load(settings.BLACK_BG_IMG)

        for y in range(0, height, background.get_height()):
            for x in range(0, width, background.get_width()):
                self.game.screen.blit(background, (x, y))

    def draw(self):
        """Draws menu on screen."""
        self.menu = KezMenu(
            ['NEW GAME', self.new_game],
            ['EXIT', self.exit])

        pos = (
            (self.game.screen.get_width() / 2 - 100),
            (self.game.screen.get_height() / 2 - 50)
        )
        self.menu.position = pos
        self.menu.color = settings.MENU_FONT_COLOR
        self.menu.focus_color = settings.MENU_FONT_FOCUS_COLOR
        self.menu.font = pygame.font.Font(
            settings.MENU_FONT,
            settings.MENU_FONT_SIZE
        )
        self.menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)

        self.running = True
        while self.running:
            self.menu.update(
                pygame.event.get(),
                self.clock.tick(settings.FPS) / 1000.
            )
            self.fill_background()
            self.menu.draw(self.game.screen)
            pygame.display.flip()
