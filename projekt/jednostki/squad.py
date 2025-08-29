import pygame
from .wojownik import Wojownik
from enum import Enum


class Positions(Enum):
    CENTER = (0, 0)
    LEFT = (-28, 0)
    RIGHT = (28, 0)
    TOP = (0, -27)
    BOTTOM = (0, 27)
    TOPLEFT = (-14, -17)
    TOPRIGHT = (14, -17)
    BOTTOMLEFT = (-14, 17)
    BOTTOMRIGHT = (14, 17)
    CENTERLEFT = (-14, 0)
    CENTERRIGHT = (14, 0)
    CENTERTOP = (0, -17)
    CENTERBOTTOM = (0, 17)


Hex_positions = [
    Positions.TOPLEFT.value,
    Positions.TOPRIGHT.value,
    Positions.LEFT.value,
    Positions.CENTER.value,
    Positions.RIGHT.value,
    Positions.BOTTOMLEFT.value,
    Positions.BOTTOMRIGHT.value,
]


class Squad(pygame.sprite.Sprite):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group)
        self.owner_id = info["owner_id"]
        self.owner = info["owner"]
        self.color = info["color"]
        self.pos = tuple(info["pos"])
        self.tile = tile
        self.wojownicy = [None for _ in range(7)]
        self.load_data(info, frakcja)
        self.hex_positions = Hex_positions
        self.strategy = info["strategy"]
        self.wzmocnienie = info["wzmocnienie"]

    @property
    def length(self):
        l = 0
        for wojownik in self.wojownicy:
            if wojownik is not None:
                l += 1
        return l

    @property
    def ruch(self):
        min_ruch = 100
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            if wojownik.ruch < min_ruch:
                min_ruch = wojownik.ruch

        return min_ruch

    @property
    def max_ruch(self):
        min_ruch = 100
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            if wojownik.jednostka["ruch"] < min_ruch:
                min_ruch = wojownik.jednostka["ruch"]

        return min_ruch

    @ruch.setter
    def ruch(self, value):
        diff = self.ruch - value
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            wojownik.ruch -= diff

    @property
    def range(self):
        max_range = -1
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            if wojownik.bronie[0]["range"] > max_range:
                max_range = wojownik.bronie[0]["range"]
        return max_range

    def draw(self, screen):
        i = 0
        for wojownik in self.wojownicy:
            if wojownik is not None:
                wojownik.draw(self.pos, self.hex_positions[i], screen)
            i += 1

    @property
    def food(self):
        food = 0
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            food += wojownik.food
        return food

    def inzynier(self) -> bool:
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            if wojownik.name == "Inżynier":
                return True
        return False

    def get_data(self):
        info = {}
        info["color"] = self.color
        info["owner"] = self.owner
        info["owner_id"] = self.owner_id
        info["pos"] = self.pos
        info["strategy"] = self.strategy
        info["wzmocnienie"] = self.wzmocnienie
        info["jednostki"] = []
        for wojownik in self.wojownicy:
            if wojownik is not None:
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
                jednostka["ruch"],
                jednostka["array_pos"],
            )
            self.wojownicy[jednostka["array_pos"]] = w

    def __len__(self):
        dl = 0
        for wojownik in self.wojownicy:
            if wojownik is not None:
                dl += 1
        return dl

    def __add__(self, other):
        for o_wojownik in other.wojownicy:
            if o_wojownik is None:
                continue
            for i in range(7):
                if self.wojownicy[i] is None:
                    self.wojownicy[i] = o_wojownik
                    break
        i = 0
        for wojownik in self.wojownicy:
            if wojownik is not None:
                wojownik.pos = i
            i += 1
        return self

    def display(self, id):
        representation = (
            f"{self.owner} ruch: {self.ruch} wzmocnienie: {self.wzmocnienie}"
        )
        return representation

    def zdrowie(self, id, value):
        if value > 0:
            self.wojownicy[id].zdrowie = value
        else:
            self.wojownicy[id] = None
            if self.length == 0:
                self.kill()
                self.tile.jednostka = None

    def heal(self, value):
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            wojownik.zdrowie += value

    @property
    def medyk(self):
        for wojownik in self.wojownicy:
            if wojownik is None:
                continue
            if wojownik.name == "Medyk":
                return True
        return False
