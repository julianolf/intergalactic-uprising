import pygame
from kezmenu3 import KezMenu

from game import settings


class Menu(object):
    """Display game options."""

    def __init__(self, game):
        """Initializes the menu.

        Args:
            game: The running game instance.
        """
        self.game = game
        self.menu = KezMenu(["NEW GAME", self.new_game], ["EXIT", self.exit])

        pos = (
            (self.game.display.current_w / 2 - 79),
            (self.game.display.current_h / 2 + 79),
        )
        self.menu.position = pos
        self.menu.color = settings.MENU_FONT_COLOR
        self.menu.focus_color = settings.MENU_FONT_FOCUS_COLOR
        self.menu.font = pygame.font.Font(
            settings.FONT, settings.MENU_FONT_SIZE
        )
        self.menu.enableEffect("raise-col-padding-on-focus", enlarge_time=0.1)
        self.running = False

    def new_game(self):
        """Starts a new game."""
        self.game.new()
        self.game.run()

    def exit(self):
        """Exit game."""
        self.running = False

    def draw(self):
        """Draws menu on screen."""
        centerx = self.game.display.current_w / 2
        title1 = {
            "text": "Intergalactic",
            "pos": (centerx - 15, 140),
            "size": settings.FONT_LG_SIZE,
        }
        title2 = {
            "text": "Uprising",
            "pos": (centerx + 108, 171),
            "size": settings.FONT_LG_SIZE,
        }
        self.running = True
        while self.running:
            self.menu.update(
                pygame.event.get(), self.game.clock.tick(settings.FPS) / 1000.0
            )
            self.game.fill_background()
            self.game.draw_text(**title1)
            self.game.draw_text(**title2)
            self.menu.draw(self.game.screen)
            pygame.display.flip()
