from ..ustawienia import *
from ..jednostki import *
from .budynek import Budynek
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


class Recruit_sample:
    def __init__(self, ruch):
        self.ruch = ruch


class Recruit(Button):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        jednostka,
        id,
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
        self.recruit_pos = recruit_pos
        self.jednostka = jednostka
        self.id = id
        self.player = player
        self.mapa = mapa
        self.x = x
        self.y = y

    def click(self):
        try:
            self.mapa.move_flag = Wojownik(
                self.jednostka,
                self.group,
                (4000, 4000),
                None,
                self.player.id,
                self.player.color,
                self.id,
            )
            r = Recruit_sample(4)
            self.mapa.correct_moves = self.mapa.possible_moves(self.x, self.y, r)
        except (ValueError, TypeError) as e:
            print(e)


class Show(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group)

    def click(self, flag):
        flag.show = not flag.show
