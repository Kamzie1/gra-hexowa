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
        self._pos = tuple(info["pos"])
        self.tile = tile
        self.budynek = frakcja["budynek"][info["id"]]
        self.name = self.budynek["nazwa"]
        self.image = AssetManager.get_asset(self.name)
        self.rect = self.image.get_frect(center=self.pos)

        self.heal = self.budynek["heal"]
        self.earn = self.budynek["earn"]
        self.id = info["id"]

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self.rect = self.image.get_frect(center=value)
        self._pos = value

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def own(self, owner, owner_id, color):
        return


class Miasto(Budynek):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group, info, tile, frakcja)
        self.podswietlenie_group = pygame.sprite.Group()
        Podswietlenie(
            f"{self.color}_podswietlenie",
            tile.pos,
            self.podswietlenie_group,
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for tile in self.podswietlenie_group:
            tile.draw(screen)
