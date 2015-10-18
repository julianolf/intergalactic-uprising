# -*- coding: utf-8 -*-

import pygame
import menu

# Initialize pygame modules
pygame.init()

# Initialize and display main menu
screen_width = 768
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
menu_pos = (screen_width / 2 - 100, screen_height / 2 - 50)
main_menu = menu.Menu(screen, menu_pos)
main_menu.draw()
