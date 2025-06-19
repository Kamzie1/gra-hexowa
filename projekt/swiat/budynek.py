import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki


class Budynek(pygame.sprite.Sprite):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group)
        self.owner_id = info["owner_id"]
        self.owner = info["owner"]
        self.color = info["color"]
        self.pos = tuple(info["pos"])
        self.tile = tile
        self.ruch = 0
        self.budynek = frakcja[info["id"]]
        self.image = pygame.image.load(
            join(folder_grafiki, self.budynek[info["color"]])
        ).convert_alpha()
        self.nazwa = self.budynek["nazwa"]
        self.rect = self.image.get_frect(center=self.pos)
        self.zdrowie = info["zdrowie"]
        self.morale = info["morale"]

        self.heal = self.budynek["heal"]
        self.earn = self.budynek["earn"]
        self.przebicie = self.budynek["przebicie"]
        self.pancerz = self.budynek["pancerz"]
        self.atak = self.budynek["atak"]
        self.koszt_ataku = self.budynek["koszt_ataku"]
        self.id = info["id"]

    """def __init__(
        self, budynek, id, pos, group, owner, owner_id, color, zdrowie=None, morale=None
    ):
        super().__init__(group)
        self.ruch = 0
        self.pos = pos
        self.image = pygame.image.load(
            join(folder_grafiki, budynek[color])
        ).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.nazwa = budynek["nazwa"]
        self.owner = owner
        self.owner_id = owner_id
        self.color = color
        if zdrowie is None:
            self.zdrowie = budynek["zdrowie"]
        else:
            self.zdrowie = zdrowie
        if morale is None:
            self.morale = budynek["morale"]
        else:
            self.morale = morale
        self.heal = budynek["heal"]
        self.earn = budynek["earn"]
        self.przebicie = budynek["przebicie"]
        self.pancerz = budynek["pancerz"]
        self.atak = budynek["atak"]
        self.koszt_ataku = budynek["koszt_ataku"]
        self.id = id"""

    def zarabiaj(self, player):
        if self.owner == player.id:
            player.gold += self.earn["gold"]

    @property
    def zdrowie(self):
        return self._zdrowie

    @zdrowie.setter
    def zdrowie(self, value):
        self._zdrowie = value
        if self._zdrowie <= 0:
            self.tile.budynek = None
            self.kill()

    def display(self):
        display = f"{self.nazwa} : {self.zdrowie} | {self.ruch} | {self.morale} | {self.przebicie} | {self.pancerz} | {self.atak}"
        return display

    def owner_display(self):
        display = f"{self.owner}"
        return display
