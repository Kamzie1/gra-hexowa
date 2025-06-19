import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik:
    # inicjalizacja
    def __init__(self, jednostka, id, color, zdrowie=None, morale=None):
        self.name = jednostka["nazwa"]
        if zdrowie is None:
            self.zdrowie = jednostka["zdrowie"]
        else:
            self.zdrowie = zdrowie
        if morale is None:
            self.morale = jednostka["morale"]
        else:
            self.morale = morale
        self.ruch = jednostka["ruch"]
        self.przebicie = jednostka["przebicie"]
        self.pancerz = jednostka["pancerz"]
        self.atak = jednostka["atak"]
        self.koszt_ataku = jednostka["koszt_ataku"]
        self.original_ruch = self.ruch
        self.original_zdrowie = self.zdrowie
        self.id = id

        self.image = pygame.image.load(
            join(f"{folder_grafiki}/jednostki-grafika", jednostka[color])
        ).convert_alpha()

    @property
    def zdrowie(self):
        return self._zdrowie

    @zdrowie.setter
    def zdrowie(self, value):
        self._zdrowie = value
        if self.zdrowie <= 0:
            raise ValueError("zdrowie poniżej zera")

    def heal(self, value):
        self.zdrowie += value
        if self.zdrowie > self.original_zdrowie:
            self.zdrowie = self.original_zdrowie

    def get_data(self):
        stan_jednostki = {
            "zdrowie": self.zdrowie,
            "morale": self.morale,
            "id": self.id,
        }
        return stan_jednostki

    def display(self, id):
        representation = f"{self.name} ({id}) : {self.zdrowie} | {self.morale} | {self.ruch} | {self.atak} | {self.przebicie} | {self.pancerz}"
        return representation
