from projekt.ustawienia import (
    menu_color,
    menu_height,
    menu_width,
    menu_pos,
    rec_panel_pos,
)
from projekt.narzedzia import pozycja_myszy_na_surface
from .buttons import Recruit, TextButton, RekrutacjaShowButton, AkcjeShowButton
import pygame
from os.path import join


class SideMenu:
    def __init__(self, mapa):
        self.surf = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        self.surf.fill(menu_color)
        self.rect = self.surf.get_frect(topleft=menu_pos)
        self.mapa = mapa
        self.rekrutacja = PoleRekrutacji(
            menu_width, menu_height, mapa, mapa.player, (0, 60)
        )
        self.akcje = Pole(menu_width, menu_height, mapa, mapa.player, (0, 60))
        self.type = 0  # 0 to rekrutacja, 1 to akcje

        self.button_group = pygame.sprite.Group()
        self.rekrutacjaButton = RekrutacjaShowButton(
            (menu_width - 10) / 2,
            40,
            (20, 20, 20),
            (0, 10),
            self.button_group,
            "Rekrutuj",
            "consolas.ttf",
            28,
            mapa.player.color,
        )
        self.akcjeButton = AkcjeShowButton(
            (menu_width - 10) / 2,
            40,
            (20, 20, 20),
            (menu_width / 2 + 5, 10),
            self.button_group,
            "Akcje",
            "consolas.ttf",
            28,
            mapa.player.color,
        )

    def fill(self):
        self.surf.fill(menu_color)

    def event(self, mouse_pos, flag, turn, id):
        if self.rect.collidepoint(mouse_pos) and flag.show:
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, menu_pos)
            flag.klikniecie_flag = False
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    self.type = button.click()
                    return
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (0, 60))
            if self.type:
                self.akcje.event(mouse_pos, turn, id)
            else:
                self.rekrutacja.event(mouse_pos, turn, id)

    def swap(self, player):
        for button in self.button_group:
            button.kill()
        self.button_group.empty()

        self.surf.fill((50, 50, 50, 70))

        self.rekrutacja = PoleRekrutacji(
            menu_width, menu_height, self.mapa, player, (0, 60)
        )
        self.akcje = Pole(menu_width, menu_height, self.mapa, player, (0, 60))

        self.rekrutacjaButton = RekrutacjaShowButton(
            (menu_width - 10) / 2,
            40,
            (20, 20, 20),
            (0, 10),
            self.button_group,
            "Rekrutuj",
            "consolas.ttf",
            28,
            player.color,
        )
        self.akcjeButton = AkcjeShowButton(
            (menu_width - 10) / 2,
            40,
            (20, 20, 20),
            (menu_width / 2 + 5, 10),
            self.button_group,
            "Akcje",
            "consolas.ttf",
            28,
            player.color,
        )

    def draw(self, screen):
        self.surf.fill(menu_color)
        self.button_group.draw(self.surf)
        if self.type:
            self.akcje.draw(self.surf)
            pygame.draw.line(
                self.surf, (230, 230, 230), (0, 50), (menu_width / 2 + 5, 50)
            )
            pygame.draw.line(
                self.surf,
                (230, 230, 230),
                (menu_width / 2 + 5, 50),
                (menu_width / 2 + 5, 10),
            )
            pygame.draw.line(
                self.surf, (230, 230, 230), (menu_width / 2 + 5, 10), (menu_width, 10)
            )
        else:
            self.rekrutacja.draw(self.surf)
            pygame.draw.line(
                self.surf,
                (230, 230, 230),
                ((menu_width - 10) / 2, 50),
                (menu_width, 50),
            )
            pygame.draw.line(
                self.surf,
                (230, 230, 230),
                ((menu_width - 10) / 2, 50),
                ((menu_width - 10) / 2, 10),
            )
            pygame.draw.line(
                self.surf, (230, 230, 230), ((menu_width - 10) / 2, 10), (0, 10)
            )
        screen.blit(self.surf, self.rect)


class Pole:
    def __init__(self, w, h, mapa, player, pos):
        self.surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.surf.get_frect(topleft=pos)
        self.player = player
        self.mapa = mapa
        self.button_group = pygame.sprite.Group()
        self.setup()

    def setup(self):
        pass

    def draw(self, screen):
        self.surf.fill((0, 0, 0, 0))
        for button in self.button_group:
            button.draw(self.surf)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos, turn, id):
        if turn % 2 == id:
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    button.click()


class PoleRekrutacji(Pole):
    def __init__(self, w, h, mapa, player, pos):
        self.group = mapa.army_group
        super().__init__(w, h, mapa, player, pos)

    def setup(self):
        x, y = 5, 5
        id = 0
        for jednostka in self.player.frakcja["jednostka"]:
            Recruit(
                40,
                40,
                "red",
                (x, y),
                jednostka,
                id,
                self.group,
                self.button_group,
                self.player.recruit_pos,
                self.player,
                self.mapa,
                self.player.x,
                self.player.y,
            )
            x += 95
            id += 1
            if x > menu_width - 25:
                x = 5
                y += 50
