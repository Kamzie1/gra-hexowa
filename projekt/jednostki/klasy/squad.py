import pygame
from .wojownik import Wojownik


class Squad(pygame.sprite.Sprite):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group)
        self.owner = info["owner"]
        self.color = info["color"]
        self.pos = tuple(info["pos"])
        self.tile = tile
        self.wojownicy = []
        self.load_data(info, frakcja)

    def draw(self, screen):
        for wojownik in self.wojownicy:
            screen.blit(wojownik.image, wojownik.image.get_frect(center=self.pos))

    def heal(self):
        for wojownik in self.wojownicy:
            wojownik.heal()

    def get_data(self):
        info = {}
        info["color"] = self.color
        info["owner"] = self.owner
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
