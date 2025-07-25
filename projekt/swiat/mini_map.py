import pygame
from projekt.ustawienia import *
from os.path import join
from projekt.narzedzia import Singleton
from .mapa import Mapa
from projekt.network import Client


class Mini_map(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.surf = pygame.Surface((Mapa_width / skala, Mapa_height / skala))
        self.mapRect = self.surf.get_frect(topright=mini_map_pos)

        self._origin = (
            -Client().player.pos[0] + srodek[0],
            -Client().player.pos[0] + srodek[1],
        )
        self.rectsurf = pygame.Surface(
            (mini_map_mouse_rect_width, mini_map_mouse_rect_height)
        )
        self.rect = self.rectsurf.get_frect(topleft=self.origin)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = self.rectsurf.get_frect(topleft=self.origin)

    def refresh(self):
        self.surf.fill("black")

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.mapRect.collidepoint(mouse_pos):
                pos_y = mouse_pos[1] - mini_map_pos[1]
                pos_x = mouse_pos[0] + mini_width - mini_map_pos[0]
                mapa_pos_y = pos_y * skala
                mapa_pos_x = pos_x * skala
                Mapa().origin = (-mapa_pos_x + srodek[0], -mapa_pos_y + srodek[1])
                Mapa().mapRect = Mapa().mapSurf.get_frect(topleft=Mapa().origin)

    def draw(self, screen):
        self.refresh()
        self.origin = (
            -Mapa().origin[0] / skala,
            -Mapa().origin[1] / skala,
        )
        for tiles in Mapa().Tile_array:
            for tile in tiles:
                self.rysuj(tile)
                if not tile.budynek is None:
                    self.rysuj(tile.budynek)
                if not tile.jednostka is None:
                    self.draw_squad(tile.jednostka.color, tile.pos)
        pygame.draw.rect(self.surf, mini_map_rect_color, self.rect, width=1)
        pygame.draw.rect(screen, (0, 0, 0), self.mapRect, width=2)
        screen.blit(self.surf, self.mapRect)

    def draw_squad(self, color, pos):
        pos = (pos[0] / skala, pos[1] / skala)
        surf = pygame.Surface((5, 5))
        rect = surf.get_frect(center=pos)
        pygame.draw.rect(self.surf, color, rect)

    def rysuj(self, obiekt):
        pos = obiekt.pos
        pos = (pos[0] / skala, pos[1] / skala)
        image = pygame.transform.scale_by(obiekt.image, 1.11111111 / skala)
        rect = image.get_frect(center=pos)
        self.surf.blit(image, rect)
