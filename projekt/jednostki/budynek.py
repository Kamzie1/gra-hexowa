import pygame
from os.path import join
from .podswietlenie import Podswietlenie
from projekt.assetMenager import AssetManager


class Budynek(pygame.sprite.Sprite):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group)
        self.owner_id = info["owner_id"]
        self.team = info["team"]
        self.owner = info["owner"]
        self.color = info["color"]
        self.pos = tuple(info["pos"])
        self.tile = tile
        self.budynek = frakcja["budynek"][info["id"]]
        self.image = AssetManager.get_unit(self.budynek["nazwa"], self.color)
        self.nazwa = self.budynek["nazwa"]
        self.rect = self.image.get_frect(center=self.pos)

        self.heal = self.budynek["heal"]
        self.earn = self.budynek["earn"]
        self.id = info["id"]
        self.podswietlenie_group = pygame.sprite.Group()
        Podswietlenie(
            f"{self.color}_podswietlenie.png",
            tile.pos,
            self.podswietlenie_group,
        )
