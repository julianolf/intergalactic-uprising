import pygame
from game import settings
from game import Menu


class Game(object):
    """Intergalactic Uprising Game"""

    def __init__(self):
        """Creates a new Game."""
        pygame.init()
        pygame.display.set_caption('Intergalactic Uprising')
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT)
        )
        self.running = False
        self.clock = pygame.time.Clock()
        self.main_menu = Menu(self)
        self.main_menu.draw()

    def new(self):
        """Initializes a new game."""
        self.running = True
        self.run()

    def run(self):
        """Game main loop."""
        while self.running:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Event handler.

        Decide which action perform based on window and keyboard events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.main_menu.draw()

    def update(self):
        """Update sprites."""
        pass

    def draw(self):
        """Put everything on screen."""
        self.screen.fill(settings.BLACK)
        pygame.display.flip()
