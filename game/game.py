import pygame
from game import settings
from game import Menu
from game import Player, Enemy, Meteor


class Game(object):
    """Intergalactic Uprising Game"""

    def __init__(self):
        """Creates a new Game."""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Intergalactic Uprising')
        self.load_resources()
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT)
        )
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.running = False
        self.clock = pygame.time.Clock()
        self.main_menu = Menu(self)
        self.main_menu.draw()

    def new(self):
        """Initializes a new game."""
        pygame.mixer.music.load(settings.MAIN_THEME_SFX)
        self.sprites.empty()
        self.enemies.empty()
        self.meteors.empty()
        self.bullets.empty()
        self.player = Player(self, groups=[self.sprites])
        for _ in range(5):
            self.spawn_enemy()
        for _ in range(4):
            self.spawn_meteor()
        self.score = 0
        self.running = True
        self.run()

    def run(self):
        """Game main loop."""
        pygame.mixer.music.play(loops=-1)
        while self.running:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

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

    def update(self):
        """Update sprites."""
        self.sprites.update()

    def draw(self):
        """Put everything on screen."""
        self.fill_background(settings.BLACK_BG_IMG)
        self.sprites.draw(self.screen)
        self.draw_text(str(self.score), (settings.WIDTH / 2, 10))
        pygame.display.flip()

    def draw_text(self, text, pos):
        """Draws a text on screen.

        Args:
            text: The text string to be draw.
            pos: The X and Y positions on screen.
        """
        font = pygame.font.Font(settings.FONT, settings.FONT_SIZE)
        surface = font.render(text, True, settings.WHITE)
        rect = surface.get_rect()
        rect.midtop = pos
        self.screen.blit(surface, rect)

    def fill_background(self, image):
        """Fill screen with a single image."""
        background = pygame.image.load(image)

        for y in range(0, settings.HEIGHT, background.get_height()):
            for x in range(0, settings.WIDTH, background.get_width()):
                self.screen.blit(background, (x, y))

    def spawn_enemy(self):
        """Spawns a new enemy."""
        Enemy(self, groups=[self.sprites, self.enemies])

    def spawn_meteor(self):
        """Spawns a new meteor."""
        Meteor(self, groups=[self.sprites, self.meteors])

    def load_resources(self):
        """Loads resource data like images and sfx."""
        self.shoot_sfx = pygame.mixer.Sound(settings.SHOOT_SFX)
        self.killed_sfx = pygame.mixer.Sound(settings.KILLED_SFX)
        self.explosion_sfx = pygame.mixer.Sound(settings.EXPLOSION_SFX)
