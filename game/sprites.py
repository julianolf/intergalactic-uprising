import pygame
import random
from game import settings
from enum import Enum


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
        self.cannon = 1
        self.lives = 3
        self.hidden = False
        self.hidden_since = 0

    def move(self):
        """Moves player on X and Y axis."""
        if self.hidden:
            return

        keys = pygame.key.get_pressed()
        # Moves player left/right/up/down.
        if keys[pygame.K_LEFT]:
            self.rect.x -= settings.SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += settings.SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= settings.SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += settings.SPEED
        # If player reaches the boundaries stop moving.
        if self.rect.right > settings.WIDTH - 10:
            self.rect.right = settings.WIDTH - 10
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.top < 30:
            self.rect.top = 30
        if self.rect.bottom > settings.HEIGHT - 10:
            self.rect.bottom = settings.HEIGHT - 10

    def shoot(self):
        """Shoots a new bullet."""
        if self.hidden:
            return

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        time_needed = 400 if self.cannon < 5 else 200
        elapsed_time = (now - self.reload > time_needed)
        if keys[pygame.K_SPACE] and elapsed_time:
            self.reload = now
            params = {
                'game': self.game,
                'speed': (0, -10),
                'groups': [self.game.sprites, self.game.bullets]
            }
            bullets = []
            if self.cannon == 1:
                bullets = [
                    {'pos': (self.rect.centerx, self.rect.top)}
                ]
            elif self.cannon == 2:
                bullets = [
                    {'pos': (self.rect.centerx - 5, self.rect.top)},
                    {'pos': (self.rect.centerx + 5, self.rect.top)}
                ]
            elif self.cannon == 3:
                bullets = [
                    {'pos': (self.rect.centerx - 22, self.rect.top + 15)},
                    {'pos': (self.rect.centerx + 22, self.rect.top + 15)}
                ]
            elif self.cannon == 4:
                bullets = [
                    {'pos': (self.rect.centerx, self.rect.top)},
                    {
                        'pos': (self.rect.centerx - 10, self.rect.top),
                        'speed': (-1, -10)
                    },
                    {
                        'pos': (self.rect.centerx + 10, self.rect.top),
                        'speed': (1, -10)
                    }
                ]
            else:
                bullets = [
                    {'pos': (self.rect.centerx - 15, self.rect.top + 15)},
                    {'pos': (self.rect.centerx + 15, self.rect.top + 15)},
                    {'pos': (self.rect.centerx - 25, self.rect.top + 15)},
                    {'pos': (self.rect.centerx + 25, self.rect.top + 15)}
                ]
            for bullet in bullets:
                bullet_params = {**params, **bullet}
                Bullet(**bullet_params)
            self.game.shoot_sfx.play()

    def hit(self):
        """Checks if the player has hit something."""
        if self.hidden:
            return

        enemies_hits = pygame.sprite.spritecollide(
            self, self.game.enemies, True, pygame.sprite.collide_circle)
        meteors_hits = pygame.sprite.spritecollide(
            self, self.game.meteors, True, pygame.sprite.collide_circle)
        pows_hits = pygame.sprite.spritecollide(
                self, self.game.pows, True, pygame.sprite.collide_circle)

        for hit in enemies_hits + meteors_hits:
            self.shield -= hit.radius * 2
            Explosion(
                self.game,
                hit.rect.center,
                [self.game.explosions, self.game.sprites],
                Explosion.Type.SMOKE
            )
            hit_type = type(hit)
            if hit_type == Enemy:
                self.game.spawn_enemy()
            elif hit_type == Meteor:
                self.game.spawn_meteor()
            if self.shield <= 0:
                self.lives -= 1
                self.shield = 100
                self.cannon = 1
                Explosion(
                    self.game,
                    self.rect.center,
                    [self.game.explosions, self.game.sprites]
                )
                self.game.killed_sfx.play()
                self.hide()
            else:
                self.game.hit_sfx.play()

        # Applys power up accordingly to its type.
        for hit in pows_hits:
            self.game.pows_sfx[hit.type.value].play()
            if hit.type == Pow.Type.BLUE:
                self.cannon += 1
            elif hit.type == Pow.Type.GREEN:
                self.shield += 10
                self.shield = 100 if self.shield > 100 else self.shield
            elif hit.type == Pow.Type.RED:
                self.lives += 1

    def update(self):
        """Update player sprite.

        Checks if the player is alive and perform
        all animations like moving and shooting.
        """
        self.hit()
        self.shoot()
        self.move()

        # Puts the player back in the game.
        if self.hidden and pygame.time.get_ticks() - self.hidden_since > 2000:
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

        Perform animations like moving and shooting.
        """
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # If enemy left screen respawn it.
        if (self.rect.top > settings.HEIGHT + 10
                or self.rect.right < -10
                or self.rect.left > settings.WIDTH + 10):
            self.spawn()


class Bullet(pygame.sprite.Sprite):
    """A bullet."""

    def __init__(self, game, pos=(0, 0), groups=[], speed=(0, -10)):
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
        self.speedx, self.speedy = speed

    def update(self):
        """Update bullet sprite.

        Performs animation moving up and checks if
        it's hit something or left the screen.
        """
        self.rect.x += self.speedx
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
                # There's a chance to get a power up by.
                if random.random() > 0.9:
                    Pow(
                        self.game,
                        hit.rect.center,
                        [self.game.pows, self.game.sprites]
                    )
                hit.kill()
                self.game.explosion_sfx.play()
                self.game.spawn_enemy()
        # If the bullet has hit a meteor just kill the bullet.
        if pygame.sprite.spritecollide(
                self, self.game.meteors, False, pygame.sprite.collide_circle):
            self.kill()
        # If the bullet has left the screen kill it.
        if (self.rect.bottom < 0
                or self.rect.right < 0
                or self.rect.left > settings.WIDTH):
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
        self.last_collision = 0

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

    def hit(self):
        """Checks if the meteor has hit another meteor."""
        for hit in pygame.sprite.spritecollide(
                self, self.game.meteors, False, pygame.sprite.collide_circle):
            # Ignore self collision.
            if hit != self:
                now = pygame.time.get_ticks()
                # If the last collision occurred at least 3s ago
                # and it did not hit the center of the meteor.
                if ((self.last_collision == 0
                    or now - self.last_collision > 2000)
                        and not hit.rect.collidepoint(self.rect.center)):
                    self.last_collision = now
                    # If the meteor hit was way too small destroy it.
                    if (self.radius > hit.radius
                            and self.radius - hit.radius > 40):
                        Explosion(
                            self.game,
                            hit.rect.center,
                            [self.game.explosions, self.game.sprites],
                            Explosion.Type.SMOKE
                        )
                        hit.kill()
                        self.game.explosion_sfx.play()
                        self.game.spawn_meteor()
                    else:
                        # Perform some changes in the meteor course.
                        if self.rect.top > hit.rect.top:
                            self.speedy += 1
                        else:
                            self.speedy = max(self.speedy - 1, 1)
                        if self.speedx > 0 != hit.speedx > 0:
                            self.speedx *= -1
                        self.rot_speed *= -1

    def update(self):
        """Update meteor sprite.

        Perform animations like moving and rotating.
        """
        self.hit()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rotate()
        # If the meteor left screen respawn it.
        if (self.rect.top > settings.HEIGHT + 10
                or self.rect.right < -10
                or self.rect.left > settings.WIDTH + 10):
            self.game.spawn_meteor()
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Explosion animation.

    Attributes:
        Type: A sub-class defining explosion types.
    """
    class Type(Enum):
        """Explosion types.

        The values indicate the position of the
        first image used to animate the explosion.
        """
        FIRE = 0
        SMOKE = 5

    def __init__(self, game, pos, groups=[], xtype=None):
        """Initializes an explosion animation.

        Args:
            game: The running game instance.
            pos: The X and Y positions on screen.
            groups: A list of pygame.sprite.Group.
            xtype: The explosion type.
        """
        super(Explosion, self).__init__(groups)
        self.game = game
        self.type = (xtype if type(xtype) == Explosion.Type
                     else Explosion.Type(0))
        self.frame = self.type.value
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
            if self.frame < self.type.value + 5:
                center = self.rect.center
                self.image = self.game.explosions_img[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
            else:
                self.kill()


class Pow(pygame.sprite.Sprite):
    """Power Up.

    Attributes:
        Type: A sub-class defining power up types.
    """
    class Type(Enum):
        """Power up types.

        Attributes:
            Blue pill: Shooting upgrade.
            Green pill: Shield restoring.
            Red pill: Life up.
        """
        BLUE = 0
        GREEN = 1
        RED = 2

    def __init__(self, game, pos, groups=[], ptype=None):
        super(Pow, self).__init__(groups)
        self.game = game
        self.type = (ptype if type(ptype) == Pow.Type
                     else Pow.Type(random.randrange(3)))
        self.image = self.game.pows_img[self.type.value]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = int(self.rect.width * .9 / 2)
        self.speedy = 2

    def update(self):
        """Update power up sprite.

        Perform animation moving the power up down
        till it leaves the screen.
        """
        self.rect.y += self.speedy
        if self.rect.top > settings.HEIGHT:
            self.kill()
