import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik(pygame.sprite.Sprite):
    # inicjalizacja
    def __init__(
        self, jednostka, group, pos, tile, owner, color, id, zdrowie=None, morale=None
    ):
        super().__init__(group)
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
        self._pos = pos
        self.tile = tile
        self.original_ruch = self.ruch
        self.original_zdrowie = self.zdrowie
        self.id = id
        self.owner = owner
        self.color = color

        self.image = pygame.image.load(
            join(f"{folder_grafiki}/jednostki-grafika", jednostka[color])
        ).convert_alpha()

        self.rect = self.image.get_frect(center=pos)

    # reprezentacja klasy w formie stringu(do debagowania: w = Wojownik(dane) print(w) wypisze info)
    def __str__(self) -> str:
        return f"Statystyki klasy: \n ruch: {self.ruch}, \n atak: {self.atak}, \n pancerz: {self.pancerz}, \n przebicie: {self.przebicie}, \n koszt_ataku: {self.koszt_ataku} \nStatystyki jednostki: \n zdrowie: {self.zdrowie}, \n morale: {self.morale} \nPOS: {self.pos} \nid: {self.id} \nimage: {self.image}"

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.rect = self.image.get_frect(center=self._pos)
