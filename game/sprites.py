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
        self.image = self.game.player_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        self.rect.centerx = settings.WIDTH / 2
        self.rect.bottom = settings.HEIGHT - 10
        self.reload = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hidden_since = 0

    def shoot(self):
        """Shoots a new bullet."""
        now = pygame.time.get_ticks()
        if now - self.reload > 400 and not self.hidden:
            self.reload = now
            pos = (self.rect.centerx, self.rect.top + 1)
            groups = [self.game.sprites, self.game.bullets]
            Bullet(self.game, pos, groups)
            self.game.shoot_sfx.play()

    def hit(self):
        """Checks if the player has hit something."""
        enemies_hits = pygame.sprite.spritecollide(
            self, self.game.enemies, False, pygame.sprite.collide_circle)
        meteors_hits = pygame.sprite.spritecollide(
            self, self.game.meteors, False, pygame.sprite.collide_circle)

        for hit in enemies_hits + meteors_hits:
            self.shield -= hit.radius * 2
            Explosion(
                self.game,
                hit.rect.center,
                [self.game.explosions, self.game.sprites],
                Explosion.XType.SMOKE
            )
            hit.spawn()  # For now let's just respawn whoever was hit.
            if self.shield <= 0:
                self.lives -= 1
                self.shield = 100
                Explosion(
                    self.game,
                    self.rect.center,
                    [self.game.explosions, self.game.sprites]
                )
                self.game.killed_sfx.play()
                self.hide()
            else:
                self.game.hit_sfx.play()

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

        # Puts the player back in the game.
        if self.hidden and pygame.time.get_ticks() - self.hidden_since > 1500:
            self.hide()

    def hide(self):
        """(Un)Hide the player."""
        self.hidden = not self.hidden
        self.hidden_since = pygame.time.get_ticks()
        self.rect.centerx = settings.WIDTH / 2
        self.rect.bottom = settings.HEIGHT + (200 if self.hidden else -10)


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
        random_image = random.choice(self.game.enemies_img)
        self.image = random_image
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        self.endurance = self.game.enemies_img.index(random_image) + 1
        self.damage = 0
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
        self.radius = int(self.rect.width * .9 / 2)
        self.rect.centerx, self.rect.bottom = pos
        self.speedy = -10

    def update(self):
        """Update bullet sprite.

        Performs animation moving up and checks if
        it's hit something or left the screen.
        """
        self.rect.y += self.speedy
        # If the bullet has hit an enemy it causes some damage.
        for hit in pygame.sprite.spritecollide(
                self, self.game.enemies, False, pygame.sprite.collide_circle):
            self.kill()
            hit.damage += 5
            # If the enemy has died the player scores.
            if hit.damage >= hit.endurance:
                self.game.score += hit.endurance
                Explosion(
                    self.game,
                    hit.rect.center,
                    [self.game.explosions, self.game.sprites]
                )
                hit.kill()
                self.game.explosion_sfx.play()
                self.game.spawn_enemy()
        # If the bullet has hit a meteor just kill the bullet.
        if pygame.sprite.spritecollide(
                self, self.game.meteors, False, pygame.sprite.collide_circle):
            self.kill()
        # If the bullet has left the screen kill it.
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    """A meteor."""

    def __init__(self, game, groups=[]):
        """Initializes a new meteor.

        Args:
            game: The running game instance.
            groups: A list of pygame.sprite.Group.
        """
        super(Meteor, self).__init__(groups)
        self.game = game
        self._image = random.choice(self.game.meteors_img)
        self.image = self._image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        self.spawn()

    def spawn(self):
        """Defines its start position and directions speed."""
        self.rect.x = random.randrange(settings.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_rotation = 0

    def rotate(self):
        """Rotates the meteor."""
        now = pygame.time.get_ticks()
        if now - self.last_rotation > 50:
            self.last_rotation = now
            self.rot = (self.rot + self.rot_speed) % 360
            image = pygame.transform.rotate(self._image, self.rot)
            center = self.rect.center
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        """Update meteor sprite.

        Perform animations like moving and rotating."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        # If the meteor left screen respawn it.
        if (self.rect.top > settings.HEIGHT + 10
                or self.rect.right < -10
                or self.rect.left > settings.WIDTH + 10):
            self.spawn()


class Explosion(pygame.sprite.Sprite):
    """Explosion animation.

    Attributes:
        XType: A sub-class defining explosion types.
    """
    class XType:
        """Explosion types.

        The values indicate the position of the
        first image used to animate the explosion.
        """
        FIRE = 0
        SMOKE = 5

    def __init__(self, game, pos, groups=[], xtype=XType.FIRE):
        """Initializes an explosion animation.

        Args:
            game: The running game instance.
            pos: The X and Y positions on screen.
            groups: A list of pygame.sprite.Group.
            xtype: The explosion type. It can be  'fr' or 'sm'.
        """
        super(Explosion, self).__init__(groups)
        self.game = game
        self.xtype = xtype
        self.frame = xtype
        self.image = self.game.explosions_img[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_update = 0

    def update(self):
        """Animates the explosion till it self destroy."""
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.frame += 1
            if self.frame < self.xtype + 5:
                center = self.rect.center
                self.image = self.game.explosions_img[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            else:
                self.kill()
