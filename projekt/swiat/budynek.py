import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki


class Budynek(pygame.sprite.Sprite):
    def __init__(
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
        self.id = id

    def zarabiaj(self, player):
        if self.owner == player.id:
            player.gold += self.earn["gold"]
