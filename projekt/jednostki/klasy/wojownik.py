import pygame
from os.path import join


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik(pygame.sprite.Sprite):
    # inicjalizacja
    def __init__(self, jednostka, group, pos, tile, owner):
        super().__init__(group)
        self.zdrowie = jednostka["zdrowie"]
        self.morale = jednostka["morale"]
        self.ruch = jednostka["ruch"]
        self.przebicie = jednostka["przebicie"]
        self.pancerz = jednostka["pancerz"]
        self.atak = jednostka["atak"]
        self.koszt_ataku = jednostka["koszt_ataku"]
        self._pos = pos
        self.tile = tile
        self.original_ruch = self.ruch
        self.original_zdrowie = self.zdrowie
        self.owner = owner

        self.image = pygame.image.load(
            join("grafika/jednostki-grafika", jednostka["image"])
        ).convert_alpha()

        self.rect = self.image.get_frect(center=pos)

    # reprezentacja klasy w formie stringu(do debagowania: w = Wojownik(dane) print(w) wypisze info)
    def __str__(self) -> str:
        return f"Statystyki klasy: \n ruch: {self.ruch}, \n atak: {self.atak}, \n pancerz: {self.pancerz}, \n przebicie: {self.przebicie}, \n koszt_ataku: {self.koszt_ataku} \nStatystyki jednostki: \n zdrowie: {self.zdrowie}, \n morale: {self.morale} \nPOS: {self.pos}"

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.rect = self.image.get_frect(center=self._pos)
