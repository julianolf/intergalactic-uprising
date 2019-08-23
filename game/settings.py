import os

# General settings.
FPS = 30
WIDTH = 720
HEIGHT = 720

# Colors definitions.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Resources path settings.
RES_DIR = os.path.join(os.path.dirname(__file__), "res")
FNT_DIR = os.path.join(RES_DIR, "font")
SND_DIR = os.path.join(RES_DIR, "sound")
SPR_DIR = os.path.join(RES_DIR, "sprite")

# Image resources.
SPRITESHEET_IMG = os.path.join(SPR_DIR, "sheet.png")
PLAYER_SPRITESHEET_IMG = os.path.join(SPR_DIR, "player_spritesheet.png")
PLAYER_IMG = (f"ship0{i:02}.png" for i in range(76))
PLAYER_ICO_IMG = "playerLife3_orange.png"
ENEMIES_SPRITESHEET_IMG = os.path.join(SPR_DIR, "enemies_spritesheet.png")
ENEMIES_IMG = (f"ship{i}{j:02}.png" for i in range(20) for j in range(60))
BOSSES_IMG = ["spaceShips_001.png"]
METEORS_IMG = (
    "meteorBrown_big1.png",
    "meteorBrown_big2.png",
    "meteorBrown_big3.png",
    "meteorBrown_big4.png",
    "meteorBrown_med1.png",
    "meteorBrown_med3.png",
    "meteorBrown_small1.png",
    "meteorBrown_small2.png",
    "meteorBrown_tiny1.png",
    "meteorBrown_tiny2.png",
    "meteorGrey_big1.png",
    "meteorGrey_big2.png",
    "meteorGrey_big3.png",
    "meteorGrey_big4.png",
    "meteorGrey_med1.png",
    "meteorGrey_med2.png",
    "meteorGrey_small1.png",
    "meteorGrey_small2.png",
    "meteorGrey_tiny1.png",
    "meteorGrey_tiny2.png",
)
EXPLOSIONS_SPRITESHEET_IMG = os.path.join(SPR_DIR, "exp_spritesheet.png")
EXPLOSIONS_IMG = (
    f"explosion{k}{i:02}.png"
    for k, r in enumerate([64, 71, 82, 74, 65])
    for i in range(r)
)
POWS_IMG = (
    "powerupBlue.png",
    "powerupGreen_bolt.png",
    "powerupRed_star.png",
    "powerupYellow_shield.png",
)
LASER_IMG = (
    "laserRed01.png",
    "laserRed06.png",
    "laserRed07.png",
    "laserRed16.png",
    "laserRed08.png",
    "laserRed10.png",
    "laserRed11.png",
    "laserRed09.png",
)
SHIELD_IMG = ["shield1.png", "shield2.png", "shield3.png"]

# SFX resources.
MAIN_THEME_SFX = os.path.join(SND_DIR, "sfx_railJet.ogg")
SHOT_SFX = os.path.join(SND_DIR, "sfx_laser2.ogg")
KILLED_SFX = os.path.join(SND_DIR, "sfx_explosion1.wav")
EXPLOSION_SFX = os.path.join(SND_DIR, "sfx_explosion2.wav")
HIT_SFX = os.path.join(SND_DIR, "sfx_hit.wav")
POWS_SFX = [os.path.join(SND_DIR, f"sfx_pow{i}.wav") for i in range(1, 5)]

# Font settings.
FONT = os.path.join(FNT_DIR, "kenvector_future.ttf")
FONT_SIZE = 18
FONT_LG_SIZE = 42

# Menu settings.
MENU_FONT_SIZE = 24
MENU_FONT_COLOR = (205, 205, 205)
MENU_FONT_FOCUS_COLOR = (255, 255, 255)

# Player settings.
SPEED = 5
