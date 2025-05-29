import pygame


# klasa wojownik, podstawowa klasa reprezentująca mechanikę każdej jednostki, czyli jej ruch i atak, dziedziczy od specjalnej klasy Sprite od pygame pozwalajacej na lepszą kontrolę w pygame
class Wojownik(pygame.sprite.Sprite):
    # inicjalizacja
    def __init__(self, zdrowie, morale, ruch, przebicie, pancerz, atak, koszt_ataku):
        self.zdrowie = zdrowie
        self.morale = morale
        self.ruch = ruch
        self.przebicie = przebicie
        self.pancerz = pancerz
        self.atak = atak
        self.koszt_ataku = koszt_ataku

    # reprezentacja klasy w formie stringu(do debagowania: w = Wojownik(dane) print(w) wypisze info)
    def __str__(self) -> str:
        return f"Statystyki klasy: \n ruch: {self.ruch}, \n atak: {self.atak}, \n pancerz: {self.pancerz}, \n przebicie: {self.przebicie}, \n koszt_ataku: {self.koszt_ataku} \nStatystyki jednostki: \n zdrowie: {self.zdrowie}, \n morale: {self.morale}"
