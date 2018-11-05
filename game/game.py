# -*- coding: utf-8 -*-

from pygame import init, display
from .menu import Menu


def start():
    # Initialize pygame modules
    init()

    # Initialize and display main menu
    screen_width = 768
    screen_height = 512
    screen = display.set_mode((screen_width, screen_height))
    menu_pos = (screen_width / 2 - 100, screen_height / 2 - 50)
    main_menu = Menu(screen, menu_pos)
    main_menu.draw()
