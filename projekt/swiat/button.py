from ..ustawienia import *
from ..jednostki import *
from os.path import join
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, color, pos, button_group, tekst=None) -> None:
        super().__init__(button_group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_frect(topleft=self.pos)
        self.tekst = tekst

    def click(self, *args):
        pass


class Recruit(Button):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        jednostka,
        group,
        button_group,
        recruit_pos,
        player,
        mapa,
        x,
        y,
    ) -> None:
        super().__init__(width, height, color, pos, button_group)
        self.group = group
        print(f"{jednostka['nazwa']}")
        self.recruit_pos = recruit_pos
        self.jednostka = jednostka
        self.player = player
        self.mapa = mapa
        self.x = x
        self.y = y
        print("button gotowy")

    def click(self):
        print(self.x, self.y)
        try:
            if self.mapa.Tile_array[self.x][self.y].jednostka is None:
                self.player.gold -= self.jednostka["cost"]
                w = Wojownik(
                    self.jednostka,
                    self.group,
                    self.recruit_pos,
                    self.mapa.Tile_array[self.x][self.y],
                    self.player.id,
                )
                self.mapa.Tile_array[self.x][self.y].jednostka = w
        except (ValueError, TypeError) as e:
            print(e)


class Show(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group)

    def click(self, flag):
        flag.show = not flag.show
