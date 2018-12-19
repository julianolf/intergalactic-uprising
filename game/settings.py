import os

# General settings.
WIDTH = 600
HEIGHT = 600
FPS = 60

# Colors definitions.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Resources path settings.
RES_DIR = os.path.join(os.path.dirname(__file__), 'res')
FNT_DIR = os.path.join(RES_DIR, 'font')
SND_DIR = os.path.join(RES_DIR, 'sound')
SPR_DIR = os.path.join(RES_DIR, 'sprite')
SPR_BG_DIR = os.path.join(SPR_DIR, 'background')
SPR_EN_DIR = os.path.join(SPR_DIR, 'enemy')
SPR_MT_DIR = os.path.join(SPR_DIR, 'meteor')
SPR_PL_DIR = os.path.join(SPR_DIR, 'player')
SPR_PW_DIR = os.path.join(SPR_DIR, 'pow')
SPR_UI_DIR = os.path.join(SPR_DIR, 'ui')
SPR_FX_DIR = os.path.join(SPR_DIR, 'fx')

# Image resources.
BLACK_BG_IMG = os.path.join(SPR_BG_DIR, 'black.png')
PLAYER_IMG = os.path.join(SPR_PL_DIR, 'player_ship1_red.png')
PLAYER_ICO_IMG = os.path.join(SPR_UI_DIR, 'player_life1_red.png')
ENEMIES_IMG = [os.path.join(SPR_EN_DIR, img) for img in (
    'enemy_black1.png', 'enemy_black2.png', 'enemy_black3.png',
    'enemy_black4.png', 'enemy_black5.png', 'enemy_blue1.png',
    'enemy_blue2.png', 'enemy_blue3.png', 'enemy_blue4.png',
    'enemy_blue5.png', 'enemy_green1.png', 'enemy_green2.png',
    'enemy_green3.png', 'enemy_green4.png', 'enemy_green5.png',
    'enemy_red1.png', 'enemy_red2.png', 'enemy_red3.png',
    'enemy_red4.png', 'enemy_red5.png'
)]
METEORS_IMG = [os.path.join(SPR_MT_DIR, img) for img in (
    'meteorBrown_big1.png', 'meteorBrown_big2.png',
    'meteorBrown_big3.png', 'meteorBrown_big4.png',
    'meteorBrown_med1.png', 'meteorBrown_med2.png',
    'meteorBrown_small1.png', 'meteorBrown_small2.png',
    'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png',
    'meteorGrey_big1.png', 'meteorGrey_big2.png',
    'meteorGrey_big3.png', 'meteorGrey_big4.png',
    'meteorGrey_med1.png', 'meteorGrey_med2.png',
    'meteorGrey_small1.png', 'meteorGrey_small2.png',
    'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png'
)]
EXPLOSIONS_IMG = [os.path.join(SPR_FX_DIR, img) for img in (
    'explosion01.png', 'explosion02.png',
    'explosion03.png', 'explosion04.png',
    'explosion05.png', 'explosion06.png',
    'explosion07.png', 'explosion08.png',
    'explosion09.png', 'explosion10.png'
)]
POWS_IMG = [os.path.join(SPR_PW_DIR, img) for img in (
    'pill_blue.png', 'pill_green.png',
    'pill_red.png', 'pill_yellow.png'
)]

# SFX resources.
MAIN_THEME_SFX = os.path.join(SND_DIR, 'sfx_railJet.ogg')
SHOOT_SFX = os.path.join(SND_DIR, 'sfx_laser2.ogg')
KILLED_SFX = os.path.join(SND_DIR, 'sfx_explosion1.wav')
EXPLOSION_SFX = os.path.join(SND_DIR, 'sfx_explosion2.wav')
HIT_SFX = os.path.join(SND_DIR, 'sfx_hit.wav')
POWS_SFX = [os.path.join(SND_DIR, f'sfx_pow{i}.wav') for i in range(1, 4)]

# Font settings.
FONT = os.path.join(FNT_DIR, 'kenvector_future.ttf')
FONT_SIZE = 18
FONT_LG_SIZE = 42

# Menu settings.
MENU_FONT_SIZE = 24
MENU_FONT_COLOR = (205, 205, 205)
MENU_FONT_FOCUS_COLOR = (255, 255, 255)

# Player settings.
SPEEDX = 5
