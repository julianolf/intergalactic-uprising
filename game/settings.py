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
SPR_PL_DIR = os.path.join(SPR_DIR, 'player')
SPR_UI_DIR = os.path.join(SPR_DIR, 'ui')

# Image resources.
BLACK_BG_IMG = os.path.join(SPR_BG_DIR, 'black.png')
PLAYER_IMG = os.path.join(SPR_PL_DIR, 'player_ship1_red.png')
ENEMIES_IMG = [os.path.join(SPR_EN_DIR, img) for img in (
    'enemy_black1.png', 'enemy_black2.png', 'enemy_black3.png',
    'enemy_black4.png', 'enemy_black5.png', 'enemy_blue1.png',
    'enemy_blue2.png', 'enemy_blue3.png', 'enemy_blue4.png',
    'enemy_blue5.png', 'enemy_green1.png', 'enemy_green2.png',
    'enemy_green3.png', 'enemy_green4.png', 'enemy_green5.png',
    'enemy_red1.png', 'enemy_red2.png', 'enemy_red3.png',
    'enemy_red4.png', 'enemy_red5.png'
)]

# Menu settings.
MENU_FONT = os.path.join(FNT_DIR, 'kenvector_future.ttf')
MENU_FONT_SIZE = 32
MENU_FONT_COLOR = (205, 205, 205)
MENU_FONT_FOCUS_COLOR = (255, 255, 255)

# Player settings.
SPEEDX = 5
