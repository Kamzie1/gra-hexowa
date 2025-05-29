import pygame


class Mapa:
    def __init__(self, Szerokosc, Wysokosc, color, pos):
        self.Wysokosc = Wysokosc
        self.Szerokosc = Szerokosc
        self.origin = pos
        self.mapSurf = pygame.Surface((self.Szerokosc, self.Wysokosc))
        self.color = color
        self.mapSurf.fill(self.color)
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)

    def fill(self):
        self.mapSurf.fill(self.color)

    def update(self):
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)


class Mini_map(Mapa):
    def __init__(self, Szerokosc, Wysokosc, color, pos):
        super().__init__(Szerokosc, Wysokosc, color, pos)
        self.mapRect = self.mapSurf.get_frect(bottomright=pos)
