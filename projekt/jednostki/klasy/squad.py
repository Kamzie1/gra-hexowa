import pygame
from .wojownik import Wojownik
from enum import Enum


class Positions(Enum):
    CENTER = (0, 0)
    LEFT = (-28, 0)
    RIGHT = (28, 0)
    TOP = (0, -27)
    BOTTOM = (0, 27)
    TOPLEFT = (-14, -13)
    TOPRIGHT = (14, -13)
    BOTTOMLEFT = (-14, 13)
    BOTTOMRIGHT = (14, 13)
    CENTERLEFT = (-14, 0)
    CENTERRIGHT = (14, 0)
    CENTERTOP = (0, -13)
    CENTERBOTTOM = (0, 13)


class Squad(pygame.sprite.Sprite):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group)
        self.owner_id = info["owner_id"]
        self.owner = info["owner"]
        self.color = info["color"]
        self.pos = tuple(info["pos"])
        self.tile = tile
        self.wojownicy = []
        self.load_data(info, frakcja)

    @property
    def ruch(self):
        min_ruch = 100
        for wojownik in self.wojownicy:
            if wojownik.ruch < min_ruch:
                min_ruch = wojownik.ruch

        return min_ruch

    @ruch.setter
    def ruch(self, value):
        diff = self.ruch - value
        for wojownik in self.wojownicy:
            wojownik.ruch -= diff

    @property
    def range(self):
        max_range = -1
        for wojownik in self.wojownicy:
            if wojownik.bronie[0]["range"] > max_range:
                max_range = wojownik.bronie[0]["range"]
        return max_range

    def draw(self, screen):
        match (len(self.wojownicy)):
            case 1:
                self.wojownicy[0].draw(self.pos, Positions.CENTER.value, screen)
            case 2:
                self.wojownicy[0].draw(self.pos, Positions.CENTERLEFT.value, screen)
                self.wojownicy[1].draw(self.pos, Positions.CENTERRIGHT.value, screen)
            case 3:
                self.wojownicy[0].draw(self.pos, Positions.LEFT.value, screen)
                self.wojownicy[2].draw(self.pos, Positions.RIGHT.value, screen)
                self.wojownicy[1].draw(self.pos, Positions.CENTERBOTTOM.value, screen)
            case 4:
                self.wojownicy[1].draw(self.pos, Positions.TOPLEFT.value, screen)
                self.wojownicy[0].draw(self.pos, Positions.TOPRIGHT.value, screen)
                self.wojownicy[2].draw(self.pos, Positions.BOTTOMLEFT.value, screen)
                self.wojownicy[3].draw(self.pos, Positions.BOTTOMRIGHT.value, screen)
            case 5:
                self.wojownicy[1].draw(self.pos, Positions.TOP.value, screen)
                self.wojownicy[0].draw(self.pos, Positions.LEFT.value, screen)
                self.wojownicy[2].draw(self.pos, Positions.CENTER.value, screen)
                self.wojownicy[3].draw(self.pos, Positions.RIGHT.value, screen)
                self.wojownicy[4].draw(self.pos, Positions.BOTTOM.value, screen)

    def get_data(self):
        info = {}
        info["color"] = self.color
        info["owner"] = self.owner
        info["owner_id"] = self.owner_id
        info["pos"] = self.pos
        info["jednostki"] = []
        for wojownik in self.wojownicy:
            info["jednostki"].append(wojownik.get_data())
        return info

    def load_data(self, info, frakcja):
        for jednostka in info["jednostki"]:
            w = Wojownik(
                frakcja[jednostka["kategoria"]][jednostka["id"]],
                jednostka["id"],
                jednostka["kategoria"],
                self.color,
                jednostka["zdrowie"],
                jednostka["morale"],
            )
            self.wojownicy.append(w)

    def __add__(self, other):
        self.wojownicy = self.wojownicy + other.wojownicy

    def display(self, id):
        representation = f"Oddział ({id}): {self.owner} | {self.ruch}"
        return representation

    def zdrowie(self, id, value):
        try:
            self.wojownicy[id].zdrowie = value
        except ValueError:
            self.wojownicy.remove(self.wojownicy[id])
            if len(self.wojownicy) == 0:
                self.kill()
                self.tile.jednostka = None

    def heal(self, value):
        for wojownik in self.wojownicy:
            wojownik.zdrowie += value
