import pygame
from .wojownik import Wojownik


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
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self.positions = [0 for _ in range(5)]
        self._pos = value
        self.positions[0] = self._pos
        self.positions[1] = (self._pos[0] + 30, self._pos[1])
        self.positions[2] = (self._pos[0] - 30, self._pos[1])
        self.positions[3] = (self._pos[0], self._pos[1] + 30)
        self.positions[4] = (self._pos[0], self._pos[1] - 30)

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

    def draw(self, screen):
        i = 0
        for wojownik in self.wojownicy:
            screen.blit(
                wojownik.image, wojownik.image.get_frect(center=self.positions[i])
            )
            i += 1

    def heal(self, value):
        for wojownik in self.wojownicy:
            wojownik.heal(value)

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
                frakcja["jednostka"][jednostka["id"]],
                jednostka["id"],
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
