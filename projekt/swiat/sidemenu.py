from projekt.ustawienia import (
    menu_color,
    menu_height,
    menu_width,
    menu_pos,
    rec_panel_pos,
)
from projekt.narzedzia import pozycja_myszy_na_surface
from .buttons import (
    Recruit,
    TextButton,
    RekrutacjaShowButton,
    AkcjeShowButton,
    Rozkaz,
    Upgrade,
    Gamble,
)
import pygame
from os.path import join
from .mapa import Mapa
from projekt.narzedzia import Singleton, MouseDisplay
from projekt.network import Client
from projekt.flag import Flag
from projekt.assetMenager import AssetManager


class SideMenu(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.surf = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        self.surf.fill(menu_color)
        self.rect = self.surf.get_frect(topleft=menu_pos)
        self.rekrutacja = PoleRekrutacji(
            menu_width, menu_height, Client().player, (0, 60)
        )
        self.akcje = PoleAkcji(menu_width, menu_height, Client().player, (0, 60))
        self.type = 0  # 0 to rekrutacja, 1 to akcje
        self.dirty = False
        self.reset = False
        self.button_group = pygame.sprite.Group()
        self.rekrutacjaButton = RekrutacjaShowButton(
            (menu_width - 10) / 2,
            60,
            (20, 20, 20),
            (0, 10),
            self.button_group,
            "Rekrutuj",
            "consolas",
            28,
            Client().player.color,
        )
        self.akcjeButton = AkcjeShowButton(
            (menu_width - 10) / 2,
            60,
            (20, 20, 20),
            (menu_width / 2 + 5, 10),
            self.button_group,
            "Akcje",
            "consolas",
            28,
            Client().player.color,
        )

    def fill(self):
        self.surf.fill(menu_color)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and Flag().show:
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, menu_pos)
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (0, 60))
            if self.type:
                self.akcje.update(mouse_pos)
            else:
                self.rekrutacja.update(mouse_pos)

    def event(self, mouse_pos):
        self.reset = False
        self.dirty = False
        if self.rect.collidepoint(mouse_pos) and Flag().show:
            self.dirty = True
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, menu_pos)
            Flag().klikniecie_flag = False
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    self.type = button.click()
                    self.reset = True
                    self.rekrutacja.refresh()
                    return
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (0, 60))
            if self.type:
                self.akcje.event(
                    mouse_pos, Client().turn, len(Client().users), Client().player.id
                )
            else:
                self.rekrutacja.event(mouse_pos, Client().turn, Client().player.id)
        else:
            self.rekrutacja.refresh()

    def swap(self, player):
        for button in self.button_group:
            button.kill()
        self.button_group.empty()

        self.surf.fill((50, 50, 50, 70))

        self.rekrutacja = PoleRekrutacji(menu_width, menu_height, player, (0, 60))
        self.akcje = PoleAkcji(menu_width, menu_height, player, (0, 60))

        self.rekrutacjaButton = RekrutacjaShowButton(
            (menu_width - 10) / 2,
            60,
            (20, 20, 20),
            (0, 10),
            self.button_group,
            "Rekrutuj",
            "consolas",
            28,
            player.color,
        )
        self.akcjeButton = AkcjeShowButton(
            (menu_width - 10) / 2,
            60,
            (20, 20, 20),
            (menu_width / 2 + 5, 10),
            self.button_group,
            "Akcje",
            "consolas",
            28,
            player.color,
        )

    def draw(self, screen):
        self.surf.fill(menu_color)
        self.button_group.draw(self.surf)
        if self.type:
            self.akcje.draw(self.surf)
            pygame.draw.line(
                self.surf, (230, 230, 230), (0, 70), (menu_width / 2 + 5, 70)
            )
            pygame.draw.line(
                self.surf,
                (230, 230, 230),
                (menu_width / 2 + 5, 70),
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
                ((menu_width - 10) / 2, 70),
                (menu_width, 70),
            )
            pygame.draw.line(
                self.surf,
                (230, 230, 230),
                ((menu_width - 10) / 2, 70),
                ((menu_width - 10) / 2, 10),
            )
            pygame.draw.line(
                self.surf, (230, 230, 230), ((menu_width - 10) / 2, 10), (0, 10)
            )
        screen.blit(self.surf, self.rect)


class Pole:
    def __init__(self, w, h, player, pos):
        self.surf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.rect = self.surf.get_frect(topleft=pos)
        self.player = player
        self.button_group = pygame.sprite.Group()
        self.setup()

    def setup(self):
        pass

    def draw(self, screen):
        self.surf.fill((0, 0, 0, 0))
        for button in self.button_group:
            button.draw(self.surf)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos, turn, user_len, id):
        if turn % user_len == id:
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    button.click()

    def update(self, mouse_pos):
        for button in self.button_group:
            if button.rect.collidepoint(mouse_pos):
                button.hover()
                MouseDisplay().update(pygame.mouse.get_pos(), button.description)


class PoleRekrutacji(Pole):
    def __init__(self, w, h, player, pos):
        self.group = Mapa().army_group
        super().__init__(w, h, player, pos)

    def setup(self):
        x, y = 5, 20
        id = 0
        for jednostka in self.player.frakcja["jednostka"]:
            Recruit(
                60,
                60,
                "red",
                (x, y),
                jednostka,
                id,
                self.button_group,
                f"{jednostka["nazwa"]} \nfood: {jednostka["food"]}",
            )
            x += 175
            id += 1
            if x + 85 > menu_width - 25:
                x = 5
                y += 120

    def refresh(self):
        for button in self.button_group:
            button.count = 0

    def event(self, mouse_pos, turn, id):
        dirty = False
        if turn % len(Client().users) == id:
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    button.click()
                    dirty = True
        if not dirty:
            SideMenu().reset = True
            self.refresh()


class PoleAkcji(Pole):
    def __init__(self, w, h, player, pos):
        super().__init__(w, h, player, pos)

    def setup(self):
        Rozkaz(
            60,
            60,
            "red",
            (5, 20),
            "zloto_rozkaz",
            self.button_group,
            """przychód złota 125% na 2 tury
            4 tury cooldown""",
        )
        Upgrade(
            60,
            60,
            "red",
            (180, 20),
            "zloto_upgrade",
            self.button_group,
            """ulepsz wydobycie zlota.
            level 2 : 110%"
            level 3 : 120%"
            level 4 : 130%""",
        )
        Upgrade(
            60,
            60,
            "blue",
            (355, 20),
            "mury_upgrade",
            self.button_group,
            """ulepsz obronę murów miasta.
            level 2 : 75%
            level 3 : 80%""",
        )
        Rozkaz(
            60,
            60,
            "blue",
            (5, 140),
            "movement_rozkaz",
            self.button_group,
            f"""zwieksz ruch wszystkich jednostek o {AssetManager.get_akcje("movement_rozkaz", "mnoznik")} na 1 turę
            3 tury cooldown""",
        )
        Rozkaz(
            60,
            60,
            "red",
            (180, 140),
            "wheater_forecast",
            self.button_group,
            f"""Odkryj przyszłą pogodę 1 tura cooldown""",
        )
        Rozkaz(
            60,
            60,
            "blue",
            (355, 140),
            "change_wheater",
            self.button_group,
            f"""Zmień na czas twojego ruchu pogodę na chmury 2 tury cooldown""",
        )
        Gamble(60, 60, "red", (5, 260), self.button_group)
