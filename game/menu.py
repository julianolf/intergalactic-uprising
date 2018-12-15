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
        self.menu = KezMenu(
            ['NEW GAME', self.new_game],
            ['EXIT', self.exit])

        pos = (
            (settings.WIDTH / 2 - 100),
            (settings.HEIGHT / 2 - 50)
        )
        self.menu.position = pos
        self.menu.color = settings.MENU_FONT_COLOR
        self.menu.focus_color = settings.MENU_FONT_FOCUS_COLOR
        self.menu.font = pygame.font.Font(
            settings.FONT,
            settings.MENU_FONT_SIZE
        )
        self.menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)
        self.running = False

    def new_game(self):
        """Starts a new game."""
        self.game.new()

    def exit(self):
        """Exit game."""
        self.running = False

    def draw(self):
        """Draws menu on screen."""
        self.running = True
        while self.running:
            self.menu.update(
                pygame.event.get(),
                self.game.clock.tick(settings.FPS) / 1000.
            )
            self.game.fill_background(self.game.black_bg_img)
            self.menu.draw(self.game.screen)
            pygame.display.flip()
