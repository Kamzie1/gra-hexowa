from ustawienia import *
from jednostki import *
from .buttton import Recruit
import pygame


class SideMenu:
    def __init__(self, player, mapa):
        self.surf = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        self.surf.fill(menu_color)
        self.rect = self.surf.get_frect(topleft=menu_pos)
        self.player = player
        self.group = player.army_group
        self.button_group = pygame.sprite.Group()
        self.recruit_group = pygame.sprite.Group()
        self.mapa = mapa

        self.recruit_surface = pygame.Surface((menu_width, 100), pygame.SRCALPHA)
        self.recruit_rec = self.recruit_surface.get_frect(topleft=(0, 0))

        Recruit(
            50,
            50,
            "red",
            (0, 0),
            Yukimura_Sanada,
            self.group,
            self.recruit_group,
            recruit_pos,
            self.player,
            self.mapa,
        )

        Recruit(
            50,
            50,
            "green",
            (0, 50),
            Bodyguard,
            self.group,
            self.recruit_group,
            recruit_pos,
            self.player,
            self.mapa,
        )

    def fill(self):
        self.surf.fill(menu_color)
