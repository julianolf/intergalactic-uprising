import pygame
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
        self.image = pygame.Surface((50, 50))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = settings.WIDTH / 2
        self.rect.bottom = settings.HEIGHT - 10

    def update(self):
        """Update player sprite.

        Checks if the player is alive and perform
        all animations like moving and shooting.
        """
        keys = pygame.key.get_pressed()
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
