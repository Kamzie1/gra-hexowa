import pygame
from os.path import join
from .miasto import Miasto
from projekt.swiat.tile import Podswietlenie


class Wioska(Miasto):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group, info, tile, frakcja)

    def own(self, new_owner, new_owner_id, new_color):
        self.owner = new_owner
        self.owner_id = new_owner_id
        self.color = new_color
        self.podswietlenie_group.empty()
        Podswietlenie(
            f"{self.color}_podswietlenie.png",
            self.pos,
            self.podswietlenie_group,
        )
        self.image = pygame.image.load(
            join("Grafika/budynki-grafika", self.budynek[self.color])
        ).convert_alpha()
