from ustawienia import *
import pygame


class SideMenu:
    def __init__(self):
        self.surf = pygame.Surface((menu_width, menu_height))
        self.surf.fill(menu_color)
        self.rect = self.surf.get_frect(topleft=menu_pos)

    def fill(self):
        self.surf.fill(menu_color)
