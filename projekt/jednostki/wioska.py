import pygame
from os.path import join
from .miasto import Miasto
from .podswietlenie import Podswietlenie
from projekt.assetMenager import AssetManager
from projekt.network import Client


class Wioska(Miasto):
    def __init__(self, group, info, tile, frakcja):
        super().__init__(group, info, tile, frakcja)
        self.podswietlenie_group.empty()
        Podswietlenie(
            f"{self.color}_podswietlenie",
            self.pos,
            self.podswietlenie_group,
        )
        self.image = AssetManager.get_asset(self.name)

    def own(self, new_owner, new_owner_id, new_color, new_team):
        if new_owner_id == 1:
            print("AI")
        self.owner = new_owner
        self.owner_id = new_owner_id
        self.team = new_team
        self.color = new_color
        self.podswietlenie_group.empty()
        Podswietlenie(
            f"{self.color}_podswietlenie",
            self.pos,
            self.podswietlenie_group,
        )
        self.image = AssetManager.get_asset(self.name)
        Client().player.medals += 10
