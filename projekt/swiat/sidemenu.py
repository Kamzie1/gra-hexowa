from ..ustawienia import *
from ..jednostki import *
from ..narzedzia import pozycja_myszy_na_surface
from .buttons import Recruit
import pygame
from os.path import join


class SideMenu:
    def __init__(self, player, mapa):
        self.surf = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        self.surf.fill(menu_color)
        self.rect = self.surf.get_frect(topleft=menu_pos)
        self.player = player
        self.group = mapa.army_group
        self.button_group = pygame.sprite.Group()
        self.recruit_group = pygame.sprite.Group()
        self.mapa = mapa

        self.recruit_surface = pygame.Surface((menu_width - 20, 300), pygame.SRCALPHA)
        self.recruit_surface.fill((50, 50, 50, 70))
        self.recruit_rec = self.recruit_surface.get_frect(topleft=rec_panel_pos)
        self.font = pygame.font.Font(join("Grafika/fonts", font), font_size)
        self.res_font = pygame.font.Font(join("Grafika/fonts", font), 10)

        self.gold_icon = pygame.image.load(join("Grafika", "złoto.png"))
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))

        display = "Rekrutuj"
        text = self.font.render(display, True, "white")
        text_rect = text.get_rect(topleft=(5, 5))
        self.recruit_surface.blit(text, text_rect)

        x, y = 5, 40
        id = 0
        for jednostka in self.player.frakcja["jednostka"]:
            self.create_recruit_button(
                jednostka,
                id,
                x,
                y,
                self.player.recruit_pos,
                self.player.x,
                self.player.y,
            )
            x += 95
            id += 1
            if x > menu_width - 25:
                x = 5
                y += 50

    def fill(self):
        self.surf.fill(menu_color)

    def event(self, mouse_pos, flag, turn, id):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, menu_pos)
        if self.rect.collidepoint(mouse_pos) and flag.show:
            flag.klikniecie_flag = False
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, rec_panel_pos)
            if turn % 2 == id:
                for button in self.recruit_group:
                    if button.rect.collidepoint(mouse_pos):
                        button.click()

    def draw(self, screen):
        self.fill()
        self.recruit_group.draw(self.recruit_surface)
        self.surf.blit(self.recruit_surface, self.recruit_rec)
        screen.blit(self.surf, self.rect)

    def create_recruit_button(
        self, jednostka, id, x, y, recruit_pos, miasto_x, miasto_y
    ):
        Recruit(
            40,
            40,
            "red",
            (x, y),
            jednostka,
            id,
            self.group,
            self.recruit_group,
            recruit_pos,
            self.player,
            self.mapa,
            miasto_x,
            miasto_y,
        )

        self.gold_rect = self.scaled_gold_icon.get_frect(topleft=(x + 45, y + 5))
        self.recruit_surface.blit(self.scaled_gold_icon, self.gold_rect)
        display = f"{jednostka["cost"]}"
        text = self.res_font.render(display, True, "white")
        text_rect = text.get_rect(topleft=(x + 60, y + 10))
        self.recruit_surface.blit(text, text_rect)
