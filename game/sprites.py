import random
from enum import Enum
from xml.dom import minidom

import pygame

from game import settings


class Spritesheet(object):
    """Manage image spritesheets."""

    def __init__(self, file_name, color_key=settings.BLACK):
        """
        Args:
            file_name (str): Spritesheet (full path) file name.
        """
        super(Spritesheet, self).__init__()
        self.image = pygame.image.load(file_name).convert()
        self.info = minidom.parse(file_name.replace(".png", ".xml"))
        self.color_key = color_key

    def get_info(self, image_name):
        """Get image position and size.

        Return where in the spritesheet the image starts and what is its size.

        Args:
            image_name (str): The image name.

        Returns:
            Four values are returned (x, y, w, h).
            x (int): X axis value.
            y (int): Y axis value.
            w (int): Image size horizontally.
            h (int): Image size vertically.

        Raises:
            ValueError: If no entry was found for image_name.
        """
        nodes = self.info.getElementsByTagName("sprite")
        for node in nodes:
            if node.getAttribute("n") == image_name:
                return map(
                    int,
                    (
                        node.getAttribute("x"),
                        node.getAttribute("y"),
                        node.getAttribute("w"),
                        node.getAttribute("h"),
                    ),
                )
        raise ValueError(f"{image_name} not found in spritesheet.")

    def get_image(self, image_name):
        """Get image by name.

        Args:
            image_name (str): The image name.

        Returns:
            A pygame.Surface instance representing the image.
        """
        x, y, width, height = self.get_info(image_name)
        image = pygame.Surface((width, height))
        image.blit(self.image, (0, 0), (x, y, width, height))
        # image = pygame.transform.scale(
        #     image, (int(width * 0.50), int(height * 0.50))
        # )
        image.set_colorkey(self.color_key)
        return image


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
        self.frames = self.game.player_img
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.game.display.current_w / 2
        self.rect.bottom = self.game.display.current_h - 10
        self.reload = 0
        self.energy = 100
        self.cannon = 1
        self.lives = 3
        self.shield = False
        self.hidden = False
        self.hidden_since = 0
        self.last_update = 0

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
        if self.rect.right > self.game.display.current_w - 10:
            self.rect.right = self.game.display.current_w - 10
        if self.rect.left < 10:
            self.rect.left = 10
        if self.rect.top < 30:
            self.rect.top = 30
        if self.rect.bottom > self.game.display.current_h - 10:
            self.rect.bottom = self.game.display.current_h - 10

    def shoot(self):
        """Shoots a new laser."""
        if self.hidden:
            return

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        time_needed = 400 if self.cannon < 5 else 200
        elapsed_time = now - self.reload > time_needed
        if keys[pygame.K_SPACE] and elapsed_time:
            self.reload = now
            params = {
                "game": self.game,
                "speed": (0, -10),
                "groups": [self.game.sprites, self.game.shots],
            }
            shots = []
            if self.cannon == 1:
                shots = [{"pos": (self.rect.centerx, self.rect.top)}]
            elif self.cannon == 2:
                shots = [
                    {"pos": (self.rect.centerx - 5, self.rect.top)},
                    {"pos": (self.rect.centerx + 5, self.rect.top)},
                ]
            elif self.cannon == 3:
                shots = [
                    {"pos": (self.rect.centerx - 22, self.rect.top + 15)},
                    {"pos": (self.rect.centerx + 22, self.rect.top + 15)},
                ]
            elif self.cannon == 4:
                shots = [
                    {"pos": (self.rect.centerx, self.rect.top)},
                    {
                        "pos": (self.rect.centerx - 10, self.rect.top),
                        "speed": (-1, -10),
                    },
                    {
                        "pos": (self.rect.centerx + 10, self.rect.top),
                        "speed": (1, -10),
                    },
                ]
            else:
                shots = [
                    {"pos": (self.rect.centerx - 15, self.rect.top + 15)},
                    {"pos": (self.rect.centerx + 15, self.rect.top + 15)},
                    {"pos": (self.rect.centerx - 25, self.rect.top + 15)},
                    {"pos": (self.rect.centerx + 25, self.rect.top + 15)},
                ]
            for shot in shots:
                shot_params = {**params, **shot}
                Laser(**shot_params)

    def hit(self):
        """Checks if the player has hit something."""
        if self.hidden:
            return

        enemies_hits = pygame.sprite.spritecollide(
            self,
            self.game.enemies,
            True,
            pygame.sprite.collide_rect_ratio(0.8),
        )
        meteors_hits = pygame.sprite.spritecollide(
            self,
            self.game.meteors,
            True,
            pygame.sprite.collide_rect_ratio(0.8),
        )
        pows_hits = pygame.sprite.spritecollide(
            self, self.game.pows, True, pygame.sprite.collide_rect_ratio(0.8)
        )

        for hit in enemies_hits + meteors_hits:
            self.energy -= hit.radius * 2
            hit.destroy()
            if self.energy <= 0:
                self.die()
            else:
                self.game.hit_sfx.play()

        # Applys power up accordingly to its type.
        for hit in pows_hits:
            self.game.pows_sfx[hit.type.value].play()
            if hit.type == Pow.Type.BLUE:
                self.cannon += 1
            elif hit.type == Pow.Type.GREEN:
                self.energy += 10
                self.energy = 100 if self.energy > 100 else self.energy
            elif hit.type == Pow.Type.RED:
                self.lives += 1
            elif hit.type == Pow.Type.YELLOW:
                if not self.shield:
                    self.shield = True
                    Shield(
                        self.game, self, [self.game.shields, self.game.sprites]
                    )

    def animate(self):
        """Animate the ship."""
        index = self.frames.index(self.image)
        index = 0 if self.image == self.frames[-1] else index + 1
        self.image = self.frames[index]

    def update(self):
        """Update player sprite.

        Checks if the player is alive and perform
        all animations like moving and shooting.
        """
        self.move()
        self.hit()
        self.shoot()
        self.animate()

        # Puts the player back in the game.
        if self.hidden and pygame.time.get_ticks() - self.hidden_since > 2000:
            self.hide()

    def hide(self):
        """(Un)Hide the player."""
        self.hidden = not self.hidden
        self.hidden_since = pygame.time.get_ticks()
        self.rect.centerx = self.game.display.current_w / 2
        self.rect.bottom = self.game.display.current_h + (
            200 if self.hidden else -10
        )

    def die(self):
        """Perform animation, play sounds, loses a life
        and regenerate the players energy."""
        Explosion(
            self.game,
            self.rect.center,
            [self.game.explosions, self.game.sprites],
        )
        self.hide()
        self.game.killed_sfx.play()
        self.lives -= 1
        self.energy = 100
        self.cannon = 1


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
        self.radius = int(self.rect.width * 0.9 / 2)
        self.endurance = self.game.enemies_img.index(random_image) + 1
        self.damage = 0
        self.spawn()

    def spawn(self):
        """Defines its start position and directions speed."""
        self.rect.x = random.randrange(
            self.game.display.current_w - self.rect.width
        )
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(1, 8)

    def move(self):
        """Updates enemy position."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def hit(self):
        """Checks if the enemy has hit something."""
        if pygame.sprite.spritecollide(
            self, self.game.shields, False, pygame.sprite.collide_circle
        ):
            self.destroy()

    def update(self):
        """Update enemy sprite.

        Perform animations like moving and shooting.
        """
        self.move()
        self.hit()

        # If enemy left screen respawn it.
        if (
            self.rect.top > self.game.display.current_h + 10
            or self.rect.right < -10
            or self.rect.left > self.game.display.current_w + 10
        ):
            self.spawn()

    def destroy(self):
        """Destroys enemy and spawn a new one."""
        if random.random() > 0.9:
            Pow(
                self.game,
                self.rect.center,
                [self.game.pows, self.game.sprites],
            )
        Explosion(
            self.game,
            self.rect.center,
            [self.game.explosions, self.game.sprites],
        )
        self.kill()
        self.game.spawn_enemy()


class Boss(pygame.sprite.Sprite):
    """A bigger and tough enemy.

    Attributes:
        State: A subclass defining the sprite state.
    """

    class State(Enum):
        """Sprite states.

        Attributes:
            ARRIVING: Tells the enemy is getting in position.
            SEEKING: Tells the enemy is seeking the player.
            ATTACKING: Tells the enemy is about to attack.
        """

        ARRIVING = 0
        SEEKING = 1
        ATTACKING = 2

    def __init__(self, game, which=None, groups=[]):
        """Initializes a new boss.

        Args:
            game: The running game instance.
            which: The positional number of the boss in the game.
            groups: A list of pygame.sprite.Group.
        """
        super(Boss, self).__init__(groups)
        self.game = game
        self.image = (
            self.game.bosses_img[which]
            if which is not None
            else random.choice(self.game.bosses_img)
        )
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        self.damage = 0
        self.rect.midtop = (
            self.game.display.current_w / 2,
            self.rect.height * -1,
        )
        self.state = Boss.State.ARRIVING

    def move(self):
        """Must be overridden.

        Updates boss position.
        """
        pass

    def shoot(self):
        """Must be overridden.

        Shoots.
        """
        pass

    def animate(self):
        """Must be overridden.

        Switches frames to animate.
        """
        pass

    def update(self):
        """Update boss sprite.

        Perform animations like moving and shooting.
        """
        self.move()
        self.shoot()
        self.animate()

    def destroy(self):
        """Destroys the boss and start the next level."""
        Explosion(
            self.game,
            self.rect.center,
            [self.game.explosions, self.game.sprites],
        )
        self.kill()
        self.game.enemies_remaining = 100
        self.game.release_mobs()


class BossOne(Boss):
    """Describes first boss moving pattern and attack."""

    def __init__(self, game, groups=[]):
        """Initializes the first boss.

        Args:
            game: The running game instance.
            groups: A list of pygame.sprite.Group.
        """
        super(BossOne, self).__init__(game, 0, groups)
        self.endurance = 300
        self.speedx = 0
        self.speedy = 0
        self.reloading = False
        self.reload_time = 0
        self.shots = 10
        self.last_shot = 0

    def move(self):
        """Updates boss position."""
        if self.state == Boss.State.ARRIVING:
            if self.rect.y < 100:
                self.speedy = 2
            else:
                self.speedy = 0
                self.gotox = self.game.player.rect.centerx
                self.state = Boss.State.SEEKING
        elif self.state == Boss.State.SEEKING:
            if self.gotox not in range(
                self.rect.centerx - 2, self.rect.centerx + 3
            ):
                self.speedx = 2 if self.rect.centerx < self.gotox else -2
            else:
                self.speedx = 0
                self.state = Boss.State.ATTACKING
        elif self.state == Boss.State.ATTACKING:
            self.gotox = self.game.player.rect.centerx

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        """Shoots."""
        if self.state == Boss.State.ATTACKING and not self.reloading:
            if self.shots:
                now = pygame.time.get_ticks()
                if now - self.last_shot > 200:
                    self.last_shot = now
                    self.shots -= 1
                    EnemyLaser(
                        self.game,
                        (self.rect.centerx - 32, self.rect.bottom + 30),
                        [self.game.enemies_shots, self.game.sprites],
                        (-2, 10),
                    )
                    EnemyLaser(
                        self.game,
                        (self.rect.centerx + 32, self.rect.bottom + 30),
                        [self.game.enemies_shots, self.game.sprites],
                        (2, 10),
                    )
            else:
                self.reloading = True
                self.reload_time = pygame.time.get_ticks()
        elif self.reloading:
            now = pygame.time.get_ticks()
            if now - self.reload_time > 1000:
                self.shots = 10
                self.reloading = False
                self.state = Boss.State.SEEKING


class Laser(pygame.sprite.Sprite):
    """A Laser shot."""

    def __init__(self, game, pos=(0, 0), groups=[], speed=(0, -10)):
        """Initializes a new laser shot.

        Args:
            game: The running game instance.
            pos: The X and Y initial position for the shot.
            groups: A list of pygame.sprite.Group.
            speed: The speed of the laser shot on X and Y axis.
        """
        super(Laser, self).__init__(groups)
        self.game = game
        self.frames = self.game.laser_img
        self.image = self.frames[1]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)
        self.rect.centerx, self.rect.bottom = pos
        self.speedx, self.speedy = speed
        self.animating = False
        self.repeat_animation = 0
        self.last_update = 0
        self.game.shot_sfx.play()

    def hit(self):
        """Checks if the shot has hit something."""
        # If the shot has hit an enemy it causes some damage.
        enemies_hits = pygame.sprite.spritecollide(
            self, self.game.enemies, False, pygame.sprite.collide_circle
        )
        bosses_hits = pygame.sprite.spritecollide(
            self, self.game.bosses, False, pygame.sprite.collide_circle
        )
        for hit in enemies_hits + bosses_hits:
            hit.damage += 5
            # If the enemy has died the player scores.
            if hit.damage >= hit.endurance:
                self.game.score += hit.endurance
                hit.destroy()
                self.kill()
            else:
                self.speedy = hit.speedy
                self.speedx = hit.speedx
                self.animating = True
        # If the shot has hit a meteor just kill the laser.
        for hit in pygame.sprite.spritecollide(
            self, self.game.meteors, False, pygame.sprite.collide_circle
        ):
            self.speedy = hit.speedy
            self.speedx = hit.speedx
            self.animating = True

    def animate(self):
        """Perform laser animation when it hits something."""
        now = pygame.time.get_ticks()
        if now - self.last_update > 90:
            self.last_update = now
            index = self.frames.index(self.image)
            if self.animating:
                if index == 7:
                    if self.repeat_animation:
                        index = 3
                        self.repeat_animation -= 1
                    else:
                        self.kill()
                        return
            else:
                index = 0 if index == 3 else index

            # Show the next frame.
            center = self.rect.center
            self.image = self.frames[index + 1]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def move(self):
        """Updates laser shot position."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def update(self):
        """Update laser shot sprite.

        Performs animation moving up and checks if
        it's hit something or left the screen.
        """
        self.move()
        if not self.animating:
            self.hit()
        self.animate()

        # If the laser shot has left the screen kill it.
        if (
            self.rect.bottom < 0
            or self.rect.right < 0
            or self.rect.left > self.game.display.current_w
        ):
            self.kill()


class EnemyLaser(Laser):
    """Enemy laser shot."""

    def hit(self):
        """Checks if the shot has hit something."""
        for hit in pygame.sprite.spritecollide(
            self, self.game.players, False, pygame.sprite.collide_circle
        ):
            hit.energy -= 35
            if hit.energy <= 0:
                hit.die()
            else:
                self.speedy = 0
                self.speedx = 0
                self.animating = True
                self.game.hit_sfx.play()
        # If the shot has hit an enemy, a meteor or a shield
        # just kill the laser.
        enemies_hits = pygame.sprite.spritecollide(
            self, self.game.enemies, False, pygame.sprite.collide_circle
        )
        meteors_hits = pygame.sprite.spritecollide(
            self, self.game.meteors, False, pygame.sprite.collide_circle
        )
        for hit in enemies_hits + meteors_hits:
            self.speedy = hit.speedy
            self.speedx = hit.speedx
            self.animating = True
        if pygame.sprite.spritecollide(
            self, self.game.shields, False, pygame.sprite.collide_circle
        ):
            self.speedy = 0
            self.speedx = 0
            self.animating = True


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
        self.radius = int(self.rect.width * 0.9 / 2)
        self.spawn()

    def spawn(self):
        """Defines its start position and directions speed."""
        self.rect.x = random.randrange(
            self.game.display.current_w - self.rect.width
        )
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
            image.set_colorkey(settings.BLACK)
            center = self.rect.center
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = center

    def hit(self):
        """Checks if the meteor has hit another meteor."""
        for hit in pygame.sprite.spritecollide(
            self, self.game.meteors, False, pygame.sprite.collide_circle
        ):
            # Ignore self collision.
            if hit != self:
                now = pygame.time.get_ticks()
                # If the last collision occurred at least 3s ago
                # and it did not hit the center of the meteor.
                if (
                    self.last_collision == 0
                    or now - self.last_collision > 2000
                ) and not hit.rect.collidepoint(self.rect.center):
                    self.last_collision = now
                    # If the meteor hit was way too small destroy it.
                    if (
                        self.radius > hit.radius
                        and self.radius - hit.radius > 40
                    ):
                        self.destroy()
                    else:
                        # Perform some changes in the meteor course.
                        if self.rect.top > hit.rect.top:
                            self.speedy += 1
                        else:
                            self.speedy = max(self.speedy - 1, 1)
                        if self.speedx > 0 != hit.speedx > 0:
                            self.speedx *= -1
                        self.rot_speed *= -1
        # If it hits a shield it has to be destroyed.
        if pygame.sprite.spritecollide(
            self, self.game.shields, False, pygame.sprite.collide_circle
        ):
            self.destroy()

    def move(self):
        """Updates the meteor position."""
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def update(self):
        """Update meteor sprite.

        Perform animations like moving and rotating.
        """
        self.move()
        self.rotate()
        self.hit()

        # If the meteor left screen respawn it.
        if (
            self.rect.top > self.game.display.current_h + 10
            or self.rect.right < -10
            or self.rect.left > self.game.display.current_w + 10
        ):
            self.game.spawn_meteor()
            self.kill()

    def destroy(self):
        """Destroys the meteor and spawn a new one."""
        Explosion(
            self.game,
            self.rect.center,
            [self.game.explosions, self.game.sprites],
            Explosion.Type.SMOKE,
        )
        self.kill()
        self.game.spawn_meteor()


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
        self.type = (
            xtype if type(xtype) == Explosion.Type else Explosion.Type(0)
        )
        self.frame = self.type.value
        self.image = self.game.explosions_img[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_update = 0
        self.game.explosion_sfx.play()

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
            Green pill: Energy restoring.
            Red pill: Life up.
            Yellow pill: Shield up.
        """

        BLUE = 0
        GREEN = 1
        RED = 2
        YELLOW = 3

    def __init__(self, game, pos, groups=[], ptype=None):
        """Initializes a power up.

        Args:
            game: The running game instance.
            pos: The X and Y positions on screen.
            groups: A list of pygame.sprite.Group.
            ptype: The power up type.
        """
        super(Pow, self).__init__(groups)
        self.game = game
        self.type = (
            ptype if type(ptype) == Pow.Type else Pow.Type(random.randrange(4))
        )
        self.image = self.game.pows_img[self.type.value]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.radius = int(self.rect.width * 0.9 / 2)
        self.speedy = 2

    def update(self):
        """Update power up sprite.

        Perform animation moving the power up down
        till it leaves the screen.
        """
        self.rect.y += self.speedy
        if self.rect.top > self.game.display.current_h:
            self.kill()


class Shield(pygame.sprite.Sprite):
    """Spaceship Shield."""

    def __init__(self, game, player, groups=[]):
        """Initializes a spaceship shield.

        Args:
            game: The running game instance.
            player: The player raising the shield.
            groups: A list of pygame.sprite.Group.
        """
        super(Shield, self).__init__(groups)
        self.game = game
        self.player = player
        self.frame = 1
        self.image = self.game.shield_img[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.player.rect.center
        self.radius = int(self.rect.width / 2)
        self.fps = 3000
        self.ttl = 6000
        self.last_update = pygame.time.get_ticks()

    def move(self):
        """Updates the shield position."""
        self.rect.center = self.player.rect.center

    def animate(self):
        """Animates the shield.

        It switches from a high to a low shield,
        after that it destroys itself.
        """
        now = pygame.time.get_ticks()
        diff = now - self.last_update
        if self.ttl <= 0:
            self.player.shield = False
            self.kill()
        elif diff > self.fps:
            self.ttl -= diff
            self.last_update = now
            self.frame -= 1
            center = self.rect.center
            self.image = self.game.shield_img[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.radius = int(self.rect.width / 2)

    def update(self):
        """Update shield sprite.

        Moves the shield in order to follow the player's spaceship
        animating the sprite till the shield time is over.
        """
        self.move()
        self.animate()
