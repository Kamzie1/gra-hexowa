import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki
from projekt.assetMenager import AssetManager


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik:
    # inicjalizacja
    def __init__(self, jednostka, id, kategoria, color, zdrowie, morale, ruch, pos):
        self.pos = pos
        self.name = jednostka["nazwa"]
        self._zdrowie = zdrowie
        self.morale = morale
        self.ruch = ruch
        self.pancerz = jednostka["pancerz"]
        self.bronie = jednostka["bronie"]
        self.atak_points = jednostka["atak_points"]
        self.kategoria = kategoria
        self.original_ruch = self.ruch
        self.original_zdrowie = self.zdrowie
        self.jednostka = jednostka
        self.id = id
        self.wzrok = jednostka["wzrok"]

        self.image = AssetManager.get_unit(self.name, color)

    @property
    def zdrowie(self):
        return self._zdrowie

    @zdrowie.setter
    def zdrowie(self, value):
        self._zdrowie = value
        if self.zdrowie <= 0:
            raise ValueError("zdrowie poniżej zera")
        if self.zdrowie > self.jednostka["zdrowie"]:
            self.zdrowie = self.jednostka["zdrowie"]

    def get_data(self):
        stan_jednostki = {
            "zdrowie": self.zdrowie,
            "morale": self.morale,
            "id": self.id,
            "kategoria": self.kategoria,
            "array_pos": self.pos,
            "ruch": self.jednostka["ruch"],
        }
        return stan_jednostki

    def display(self, id):
        representation = f"{self.name} ({id}) : {self.zdrowie} | {self.morale} | {self.ruch} | {self.bronie[0]["atak"]} | {self.atak_points} | {self.bronie[0]["range"]}"
        return representation

    def draw(self, pos, offset, screen):
        rect = self.image.get_frect(center=(pos[0] + offset[0], pos[1] + offset[1]))
        screen.blit(self.image, rect)
