import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik:
    # inicjalizacja
    def __init__(self, jednostka, id, kategoria, color, zdrowie, morale):
        self.name = jednostka["nazwa"]
        self._zdrowie = zdrowie
        self.morale = morale
        self.ruch = jednostka["ruch"]
        self.przebicie = jednostka["przebicie"]
        self.pancerz = jednostka["pancerz"]
        self.atak = jednostka["atak"]
        self.koszt_ataku = jednostka["koszt_ataku"]
        self.atak_points = jednostka["atak_points"]
        self.range = jednostka["range"]
        self.kategoria = kategoria
        self.original_ruch = self.ruch
        self.original_zdrowie = self.zdrowie
        self.jednostka = jednostka
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
        if self.zdrowie > self.jednostka["zdrowie"]:
            self.zdrowie = self.jednostka["zdrowie"]

    def get_data(self):
        stan_jednostki = {
            "zdrowie": self.zdrowie,
            "morale": self.morale,
            "id": self.id,
            "kategoria": self.kategoria,
        }
        return stan_jednostki

    def display(self, id):
        representation = f"{self.name} ({id}) : {self.zdrowie} | {self.morale} | {self.ruch} | {self.atak} | {self.atak_points} | {self.range}"
        return representation

    def draw(self, pos, offset, screen):
        rect = self.image.get_frect(center=(pos[0] + offset[0], pos[1] + offset[1]))
        screen.blit(self.image, rect)
