import pygame
from os.path import join


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik(pygame.sprite.Sprite):
    # inicjalizacja
    def __init__(self, jednostka, group, pos):
        super().__init__(group)
        self.zdrowie = jednostka["zdrowie"]
        self.morale = jednostka["morale"]
        self.ruch = jednostka["ruch"]
        self.przebicie = jednostka["przebicie"]
        self.pancerz = jednostka["pancerz"]
        self.atak = jednostka["atak"]
        self.koszt_ataku = jednostka["koszt_ataku"]
        self.pos = pos

        try:
            if not pygame.display.get_init():
                pygame.display.init()
                pygame.display.set_mode((1, 1))
            self.image = pygame.image.load(
                join("grafika", jednostka["image"])
            ).convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_frect(center=pos)
        if self.rect is None:
            raise ValueError("błąd rect klasa wojownika")

    # reprezentacja klasy w formie stringu(do debagowania: w = Wojownik(dane) print(w) wypisze info)
    def __str__(self) -> str:
        return f"Statystyki klasy: \n ruch: {self.ruch}, \n atak: {self.atak}, \n pancerz: {self.pancerz}, \n przebicie: {self.przebicie}, \n koszt_ataku: {self.koszt_ataku} \nStatystyki jednostki: \n zdrowie: {self.zdrowie}, \n morale: {self.morale}"

    def marsz(self):
        self.rect.x += self.ruch / 10  # type: ignore
