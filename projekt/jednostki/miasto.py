import pygame
from os.path import join
from .podswietlenie import Podswietlenie
from projekt.assetMenager import AssetManager


class Miasto(pygame.sprite.Sprite):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group)
        self.owner_id = info["owner_id"]
        self.owner = info["owner"]
        self.color = info["color"]
        self.pos = tuple(info["pos"])
        self.tile = tile
        self.budynek = frakcja["budynek"][info["id"]]
        self.name = self.budynek["nazwa"]
        self.image = AssetManager.get_asset(self.name)
        self.rect = self.image.get_frect(center=self.pos)

        self.heal = self.budynek["heal"]
        self.earn = self.budynek["earn"]
        self.id = info["id"]
        self.koszt_ruchu = self.budynek["ruch"]
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

    def own(self, owner, owner_id, color):
        return
