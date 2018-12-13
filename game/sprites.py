import pygame
import random
from game import settings


class Player(pygame.sprite.Sprite):
    """Player's spaceship."""

    def __init__(self, game, groups=[]):
        """Initializes a new player.

        Args:
            game: The running game instance.
            groups: A list of pygame.sprite.Group.
        """
        super(Player, self).__init__(groups)
        self.game = game
        self.image = pygame.image.load(settings.PLAYER_IMG)
        self.rect = self.image.get_rect()
        self.rect.centerx = settings.WIDTH / 2
        self.rect.bottom = settings.HEIGHT - 10
        self.reload = 0

    def shoot(self):
        """Shoots a new bullet."""
        now = pygame.time.get_ticks()
        if now - self.reload > 300:
            self.reload = now
            pos = (self.rect.centerx, self.rect.top + 1)
            groups = [self.game.sprites, self.game.bullets]
            Bullet(self.game, pos, groups)

    def hit(self):
        """Checks if the player has hit something."""
        if pygame.sprite.spritecollide(self, self.game.enemies, False):
            self.game.running = False

    def update(self):
        """Update player sprite.

        Checks if the player is alive and perform
        all animations like moving and shooting.
        """
        self.hit()

        keys = pygame.key.get_pressed()
        # Shoot shoot shoot!
        if keys[pygame.K_SPACE]:
            self.shoot()
        # Moves player left/right.
        if keys[pygame.K_LEFT]:
            self.rect.x -= settings.SPEEDX
        if keys[pygame.K_RIGHT]:
            self.rect.x += settings.SPEEDX
        # If player reaches the x-boundaries stop moving.
        if self.rect.right > settings.WIDTH:
            self.rect.right = settings.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Enemy(pygame.sprite.Sprite):
    """Enemies spaceship."""

    def __init__(self, game, groups=[]):
        """Initializes a new enemy.

        Args:
            game: The running game instance.
            groups: A list of pygame.sprite.Group.
        """
        super(Enemy, self).__init__(groups)
        self.game = game
        self.image = pygame.image.load(random.choice(settings.ENEMIES_IMG))
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        """Defines its start position and directions speed."""
        self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def update(self):
        """Update enemy sprite.

        Perform animations like moving and shooting."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # If enemy left screen respawn it.
        if (self.rect.top > settings.HEIGHT + 10
                or self.rect.right < -10
                or self.rect.left > settings.WIDTH + 10):
            self.spawn()


class Bullet(pygame.sprite.Sprite):
    """A bullet."""

    def __init__(self, game, pos=(0, 0), groups=[]):
        """Initializes a new bullet.

        Args:
            game: The running game instance.
            pos: The X and Y initial position for the bullet.
            groups: A list of pygame.sprite.Group.
        """
        super(Bullet, self).__init__(groups)
        self.game = game
        self.image = pygame.Surface((5, 5))
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = pos
        self.speedy = -10

    def update(self):
        """Update bullet sprite.

        Performs animation moving up and checks if
        it's hit something or left the screen.
        """
        self.rect.y += self.speedy
        # If the bullet has hit an enemy kill both,
        # the enemy and the bullet. Also spawns a
        # new enemy for each one killed.
        for hit in pygame.sprite.groupcollide(
                self.game.bullets, self.game.enemies, True, True):
            self.game.spawn_enemy()
        # If the bullet has left the screen kill it.
        if self.rect.bottom < 0:
            self.kill()
