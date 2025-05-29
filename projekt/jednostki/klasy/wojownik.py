import pygame


class Wojownik:
    def __init__(self, zdrowie, morale, ruch, przebicie, pancerz, atak, koszt_ataku):
        self.zdrowie = zdrowie
        self.morale = morale
        self.ruch = ruch
        self.przebicie = przebicie
        self.pancerz = pancerz
        self.atak = atak
        self.koszt_ataku = koszt_ataku

    def __str__(self) -> str:
        return f"Statystyki klasy: \n ruch: {self.ruch}, \n atak: {self.atak}, \n pancerz: {self.pancerz}, \n przebicie: {self.przebicie}, \n koszt_ataku: {self.koszt_ataku} \nStatystyki jednostki: \n zdrowie: {self.zdrowie}, \n morale: {self.morale}"
