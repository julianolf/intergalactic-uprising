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
        pygame.mixer.music.load(settings.MAIN_THEME_SFX)
        self.load_resources()
        pygame.display.set_icon(self.icon_img)
        pygame.display.set_caption('Intergalactic Uprising')
        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT)
        )
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.pows = pygame.sprite.Group()
        self.running = False
        self.clock = pygame.time.Clock()
        self.main_menu = Menu(self)
        self.main_menu.draw()

    def new(self):
        """Initializes a new game."""
        self.sprites.empty()
        self.enemies.empty()
        self.meteors.empty()
        self.shots.empty()
        self.explosions.empty()
        self.pows.empty()
        self.player = Player(self, groups=[self.sprites])
        for _ in range(5):
            self.spawn_enemy()
        for _ in range(4):
            self.spawn_meteor()
        self.score = 0
        self.running = True

    def run(self):
        """Game main loop."""
        pygame.mixer.music.play(loops=-1)
        while self.running:
            self.clock.tick(settings.FPS)
            self.events()
            self.update()
            self.draw()
            self.over()
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
                if event.key == pygame.K_RETURN and not self.player.alive():
                    self.new()

    def update(self):
        """Update sprites."""
        self.sprites.update()

    def draw(self):
        """Put everything on screen."""
        self.fill_background(self.black_bg_img)
        self.sprites.draw(self.screen)
        self.draw_text(str(self.score), (settings.WIDTH / 2, 10))
        self.draw_bar((self.player.shield / 100), (75, 15))
        self.draw_lives()
        if not self.player.alive():
            # Show game over message.
            centerx, centery = settings.WIDTH / 2, settings.HEIGHT / 2
            self.draw_text(
                'Game Over', (centerx, centery - 48), settings.FONT_LG_SIZE)
            self.draw_text('[Return] play again.', (centerx, centery + 24))
            self.draw_text('[Escape] main menu.', (centerx, centery + 48))
        pygame.display.flip()

    def draw_text(self, text, pos,
                  size=settings.FONT_SIZE, color=settings.WHITE):
        """Draws a text on screen.

        Args:
            text: The text string to be draw.
            pos: The X and Y positions on screen.
            size: Text size.
            color: Text color.
        """
        font = pygame.font.Font(settings.FONT, size)
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        rect.midtop = pos
        self.screen.blit(surface, rect)

    def draw_bar(self, percent, pos, color=None):
        """Draws a status bar on screen.

        Args:
            percent: The percentage of the bar to be filled.
            pos: The X and Y positions on screen.
            color: The color for the filled area of the bar.
        """
        x, y = pos
        width, height = 100, 10
        fill = percent * width
        if not color:
            if percent < .2:
                color = settings.RED
            elif percent < .5:
                color = settings.YELLOW
            else:
                color = settings.GREEN
        outline = pygame.Rect(x, y, width, height)
        filled = pygame.Rect(x, y, fill, height)
        pygame.draw.rect(self.screen, color, filled)
        pygame.draw.rect(self.screen, settings.WHITE, outline, 2)

    def draw_lives(self):
        """Draws player's lives."""
        icon_rect = self.player_ico_img.get_rect()
        icon_rect.center = (25, 20)
        lives = self.player.lives
        if lives:
            lives -= 1
        self.screen.blit(self.player_ico_img, icon_rect)
        self.draw_text(str(lives), (60, 10))

    def fill_background(self, image):
        """Fill screen with a single image."""
        for y in range(0, settings.HEIGHT, image.get_height()):
            for x in range(0, settings.WIDTH, image.get_width()):
                self.screen.blit(image, (x, y))

    def spawn_enemy(self):
        """Spawns a new enemy."""
        Enemy(self, groups=[self.sprites, self.enemies])

    def spawn_meteor(self):
        """Spawns a new meteor."""
        Meteor(self, groups=[self.sprites, self.meteors])

    def load_resources(self):
        """Loads resource data like images and sfx."""
        self.icon_img = pygame.image.load(settings.ICON_IMG)
        self.black_bg_img = pygame.image.load(settings.BLACK_BG_IMG)
        self.player_img = pygame.image.load(settings.PLAYER_IMG)
        self.player_ico_img = pygame.image.load(settings.PLAYER_ICO_IMG)
        self.enemies_img = [pygame.image.load(e) for e in settings.ENEMIES_IMG]
        self.meteors_img = [pygame.image.load(m) for m in settings.METEORS_IMG]
        self.explosions_img = [
            pygame.image.load(e)
            for e in settings.EXPLOSIONS_IMG
        ]
        self.pows_img = [pygame.image.load(p) for p in settings.POWS_IMG]
        self.laser_img = [pygame.image.load(l) for l in settings.LASER_IMG]
        self.shot_sfx = pygame.mixer.Sound(settings.SHOT_SFX)
        self.killed_sfx = pygame.mixer.Sound(settings.KILLED_SFX)
        self.explosion_sfx = pygame.mixer.Sound(settings.EXPLOSION_SFX)
        self.hit_sfx = pygame.mixer.Sound(settings.HIT_SFX)
        self.pows_sfx = [pygame.mixer.Sound(s) for s in settings.POWS_SFX]

    def over(self):
        """Checks if the game is over."""
        if self.player.lives == 0 and not self.explosions.sprites():
            # Kill the player after losing all lives.
            self.player.kill()
