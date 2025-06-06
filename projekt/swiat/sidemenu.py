from ..ustawienia import *
from ..jednostki import *
from .button import Recruit
import pygame
from os.path import join


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

        self.recruit_surface = pygame.Surface((menu_width - 20, 300), pygame.SRCALPHA)
        self.recruit_surface.fill((50, 50, 50, 50))
        self.recruit_rec = self.recruit_surface.get_frect(topleft=rec_panel_pos)
        self.font = pygame.font.Font(join(folder_grafiki, font), font_size)
        self.res_font = pygame.font.Font(join(folder_grafiki, font), 10)

        self.gold_icon = pygame.image.load(join("grafika", "złoto.png"))
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))

        display = "Rekrutuj"
        text = self.font.render(display, True, "white")
        text_rect = text.get_rect(topleft=(5, 5))
        self.recruit_surface.blit(text, text_rect)

        self.create_recruit_button(Yukimura_Sanada, 5, 40)

        self.create_recruit_button(Bodyguard, 100, 40)

    def fill(self):
        self.surf.fill(menu_color)

    def create_recruit_button(self, jednostka, x, y):
        Recruit(
            40,
            40,
            "red",
            (x, y),
            jednostka,
            self.group,
            self.recruit_group,
            recruit_pos,
            self.player,
            self.mapa,
        )

        self.gold_rect = self.scaled_gold_icon.get_frect(topleft=(x + 45, y + 5))
        self.recruit_surface.blit(self.scaled_gold_icon, self.gold_rect)
        display = f"{jednostka["cost"]}"
        text = self.res_font.render(display, True, "white")
        text_rect = text.get_rect(topleft=(x + 60, y + 10))
        self.recruit_surface.blit(text, text_rect)
