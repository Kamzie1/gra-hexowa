import pygame
from os.path import join
from projekt.narzedzia import oslab_kolor, calc_scaled_offset, pozycja_myszy_na_surface
from projekt.jednostki import Hex_positions, Squad
from projekt.narzedzia import Przycisk
from projekt.assetMenager import AssetManager
from projekt.narzedzia import Singleton
from projekt.network import Client


class SquadDisplay(metaclass=Singleton):
    def __init__(self, width, height, pos, color):
        if hasattr(self, "_initialized"):
            return
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_frect(center=pos)
        self.pos = pos
        self.font = AssetManager.get_font("consolas", 26)
        self.wojownik_font = AssetManager.get_font("consolas", 20)
        self.font_color = color
        self.show = False
        self.skala = 4
        self.start = (self.pos[0] / 4, self.pos[1] / 2)
        self.selected = None
        self.positions_group = pygame.sprite.Group()
        self.set_up()
        self.split = Przycisk(
            120,
            30,
            "red",
            (self.width - 140, 70),
            "Rozdziel",
            "white",
        )

    def set_up(self):
        self.set_positions()

    def set_positions(self):
        i = 0
        for pos in Hex_positions:
            Pozycja(pos, self.start, 50, 50, self.positions_group, self.skala, i)
            i += 1

    def display(self, squad, screen):
        self.surf.fill("white")
        self.display_formation(squad)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, squad.color, self.rect, 4)

    def display_formation(self, squad):
        self.display_hex()
        self.display_squad(squad, (20, 20), 0, self.font)
        self.display_army(squad)
        self.display_selected()

    def display_hex(self):
        width = 56 * self.skala
        height = 54 * self.skala

        pygame.draw.line(
            self.surf,
            "black",
            (self.start[0] - width, self.start[1] + height / 2),
            (self.start[0] - width, self.start[1] - height / 2),
        )
        pygame.draw.line(
            self.surf,
            "black",
            (self.start[0] - width, self.start[1] - height / 2),
            (self.start[0], self.start[1] - height),
        )
        pygame.draw.line(
            self.surf,
            "black",
            (self.start[0], self.start[1] - height),
            (self.start[0] + width, self.start[1] - height / 2),
        )
        pygame.draw.line(
            self.surf,
            "black",
            (self.start[0] + width, self.start[1] - height / 2),
            (self.start[0] + width, self.start[1] + height / 2),
        )
        pygame.draw.line(
            self.surf,
            "black",
            (self.start[0] + width, self.start[1] + height / 2),
            (self.start[0], self.start[1] + height),
        )
        pygame.draw.line(
            self.surf,
            "black",
            (self.start[0], self.start[1] + height),
            (self.start[0] - width, self.start[1] + height / 2),
        )

    def display_army(self, squad):
        i = 0
        for pozycja in self.positions_group:
            pozycja.wojownik = squad.wojownicy[i]
            pozycja.display(self.surf, squad.color)
            i += 1

    def display2(self, squad, screen):
        self.surf.fill("white")
        self.display_wojownik(squad, (20, 20), 0, self.font)
        y = int(self.width / 20) * 2
        i = 1
        for wojownik in squad.wojownicy:
            if wojownik is None:
                continue
            self.display_wojownik(
                wojownik, (40, y + i * int(self.width / 20)), i, self.wojownik_font
            )
            i += 1
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, squad.color, self.rect, 4)

    def display_selected(self):
        if self.selected is None:
            return
        if self.selected.wojownik is None:
            return
        self.display_description()
        self.split.draw(self.surf)

    def display_description(self):
        pos = (self.pos[0] / 2, 0)
        wojownik = self.selected.wojownik
        self.display_text((50, 30), pos, wojownik.name, self.font)
        statystyki = f"""
        zdrowie : {wojownik.zdrowie}
        morale: {wojownik.morale}
        ruch: {wojownik.ruch}
        pancerz : {wojownik.pancerz}
        wzrok : {wojownik.jednostka["wzrok"]}
        atak : {wojownik.bronie[0]["atak"]}
        przebicie : {wojownik.bronie[0]["przebicie"]}
        zasięg : {wojownik.bronie[0]["range"]}
        koszt ataku : {wojownik.bronie[0]["koszt_ataku"]} 
        punkty ataku : {wojownik.atak_points}
        """
        self.display_text((self.width / 32, 100), pos, statystyki, self.wojownik_font)

    def display_text(self, offset, pos, text, font):
        text_surf = font.render(text, True, "black")
        text_rect = text_surf.get_frect(
            topleft=(pos[0] + offset[0], pos[1] + offset[1])
        )
        self.surf.blit(text_surf, text_rect)

    def display_squad(self, wojownik, pos, id, font):
        display = wojownik.display(id)
        text = font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=pos)
        self.surf.blit(text, text_rect)

    def update(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        for pozycja in self.positions_group:
            pozycja.hover(mouse_pos)

    def event(self, mouse_pos, squad, id, mapa):
        if_selected = False
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        for pozycja in self.positions_group:
            if pozycja.rect.collidepoint(mouse_pos):
                if self.selected is not None and self.selected.wojownik is not None:
                    if squad.owner_id != id or self.selected.wojownik.name == "Miasto":
                        return
                    self.swap(pozycja, squad)
                self.selected = pozycja
                pozycja.color = (200, 200, 200)
                if_selected = True
            else:
                pozycja.color = "white"

        if self.split.rect.collidepoint(mouse_pos) and squad.owner_id == id:
            self.split_formation(mapa, squad)

        if not if_selected:
            self.selected = None

    def swap(self, pozycja, squad):
        squad.wojownicy[self.selected.id].pos = pozycja.id
        if pozycja.wojownik is not None:
            squad.wojownicy[pozycja.id].pos = self.selected.id

        bufor = squad.wojownicy[self.selected.id]
        squad.wojownicy[self.selected.id] = squad.wojownicy[pozycja.id]
        squad.wojownicy[pozycja.id] = bufor

        bufor = self.selected.wojownik
        self.selected.wojownik = pozycja.wojownik
        pozycja.wojownik = bufor

    def split_formation(self, mapa, squad):
        mapa.split = self.selected.id
        info = {}
        info["color"] = squad.color
        info["owner"] = squad.owner
        info["owner_id"] = squad.owner_id
        info["pos"] = squad.pos
        info["jednostki"] = []
        jednostka = self.selected.wojownik.get_data()
        jednostka["array_pos"] = self.selected.wojownik.pos
        jednostka["ruch"] = self.selected.wojownik.ruch
        info["jednostki"].append(jednostka)
        mapa.move_flag = Squad(mapa.army_group, info, None, Client().player.frakcja)
        mapa.move_flag.tile = squad.tile
        mapa.correct_moves = mapa.possible_moves(
            squad.tile.x, squad.tile.y, mapa.move_flag
        )
        mapa.move_group.empty()
        self.show = False


class Pozycja(pygame.sprite.Sprite):
    def __init__(self, offset, start, width, height, group, skala, id):
        super().__init__(group)
        self.surf = pygame.Surface((width, height))
        self.color = "white"
        self.surf.fill(self.color)
        self.pos = calc_scaled_offset(offset, start, skala * 1.5)
        self.rect = self.surf.get_frect(center=self.pos)
        self.wojownik = None
        self.id = id
        self.healthbar = pygame.Surface((10, 60))
        self.healthbar.fill("white")
        self.healthbar_rect = self.healthbar.get_frect(
            center=(self.pos[0] - 45, self.pos[1])
        )

    def hover(self, mouse_pos):
        if self.color == (200, 200, 200):
            return
        if self.rect.collidepoint(mouse_pos):
            self.color = (220, 220, 220)
        else:
            self.color = "white"

    def display(self, screen, color):
        self.surf.fill(self.color)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "black", self.rect, width=1)
        if self.wojownik is None:
            return
        surf = AssetManager.get_unit(self.wojownik.name, color)
        rect = surf.get_frect(center=self.pos)
        screen.blit(surf, rect)
        self.display_health(screen)

    def display_health(self, screen):
        if self.wojownik is None:
            return
        procent = self.wojownik.zdrowie / self.wojownik.jednostka["zdrowie"]
        screen.blit(self.healthbar, self.healthbar_rect)
        health = pygame.Surface((10, 60 * procent))
        if procent < 0.25:
            health.fill("red")
        else:
            health.fill("green")
        screen.blit(
            health, health.get_frect(bottomleft=(self.pos[0] - 50, self.pos[1] + 30))
        )
        pygame.draw.rect(screen, "black", self.healthbar_rect, width=1)
