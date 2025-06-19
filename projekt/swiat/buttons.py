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
        info = {}
        info["color"] = self.player.color
        info["owner"] = self.player.name
        info["owner_id"] = self.player.id
        info["pos"] = (5000, 5000)
        info["jednostki"] = []
        jednostka = self.jednostka
        info["jednostki"].append(jednostka)
        print("Recruit")
        self.mapa.move_flag = Squad(self.group, info, None, self.player.frakcja)
        r = Recruit_sample(4)
        self.mapa.correct_moves = self.mapa.possible_moves(self.x, self.y, r)
        self.mapa.move_group.empty()


class Show(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group)

    def click(self, flag):
        flag.show = not flag.show


class Leave(Button):
    def __init__(self, width, height, color, pos, button_group, tekst=None):
        super().__init__(width, height, color, pos, button_group, tekst)

    def click(self, client, koniecGry):
        client.end_game(-1, koniecGry)


class SquadButtonDisplay:
    def __init__(self, width, height, color, pos, tekst=None):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_frect(midbottom=self.pos)
        self.tekst = tekst

    def event(self, mouse_pos, squadDisplay, move_flag):
        if move_flag is None:
            return
        if self.rect.collidepoint(mouse_pos):
            self.click(squadDisplay)

    def click(self, squadDisplay):
        squadDisplay.show = not squadDisplay.show
