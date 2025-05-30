import pygame
from os.path import join


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik(pygame.sprite.Sprite):
    # inicjalizacja
    def __init__(
        self, zdrowie, morale, ruch, przebicie, pancerz, atak, koszt_ataku, image, pos
    ):
        self.zdrowie = zdrowie
        self.morale = morale
        self.ruch = ruch
        self.przebicie = przebicie
        self.pancerz = pancerz
        self.atak = atak
        self.koszt_ataku = koszt_ataku
        self.pos = pos

        try:
            if not pygame.display.get_init():
                pygame.display.init()
                pygame.display.set_mode((1, 1))
            self.surf = pygame.image.load(join("grafika", image)).convert_alpha()
        except (FileNotFoundError, pygame.error):
            self.surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.surf.get_frect(center=pos)
        if self.rect is None:
            raise ValueError("błąd rect klasa wojownika")

    # reprezentacja klasy w formie stringu(do debagowania: w = Wojownik(dane) print(w) wypisze info)
    def __str__(self) -> str:
        return f"Statystyki klasy: \n ruch: {self.ruch}, \n atak: {self.atak}, \n pancerz: {self.pancerz}, \n przebicie: {self.przebicie}, \n koszt_ataku: {self.koszt_ataku} \nStatystyki jednostki: \n zdrowie: {self.zdrowie}, \n morale: {self.morale}"

    def marsz(self):
        self.rect.x += self.ruch / 10  # type: ignore
