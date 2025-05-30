import pygame
from ustawienia import *
from pytmx.util_pygame import load_pygame
from os.path import join
from .tile import Tile


class Mapa:
    def __init__(self, Szerokosc, Wysokosc, pos):
        self.Wysokosc = Wysokosc
        self.Szerokosc = Szerokosc
        self.origin = pos
        self.mapSurf = pygame.Surface((self.Szerokosc, self.Wysokosc))
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)
        self.tmx = load_pygame(join("grafika", plik_mapy))
        self.tiles_group = pygame.sprite.Group()
        self.load_tiles()

    def update(self, original_origin, original_pos) -> None:
        # aktualizacja pozycji mapy względem ekranu
        mouse_pos = pygame.mouse.get_pos()
        offset = (
            mouse_pos[0] - original_pos[0],  # type: ignore (mój pylance świruje, więc to wyłącza podświetlenie błędu)
            mouse_pos[1] - original_pos[1],  # type: ignore
        )
        if self.validateOffset(offset, original_origin):
            self.origin = (
                original_origin[0] + offset[0],  # type: ignore
                original_origin[1] + offset[1],  # type: ignore
            )
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)

    def validateOffset(self, offset, original_origin) -> bool:
        # sprawdza, czy nie wychodzisz poza mapę
        if original_origin[0] + offset[0] > mapa_x_offset:
            return False
        if original_origin[0] + offset[0] + self.Szerokosc < Width - mapa_x_offset:
            return False
        if original_origin[1] + offset[1] > mapa_y_offset:
            return False
        if original_origin[1] + offset[1] + self.Wysokosc < Height - mapa_y_offset:
            return False
        return True

    def load_tiles(self):
        # loaduje z tmx tilesy i przypisuje je do grupy
        for layer in self.tmx.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    if y % 2 == 0:
                        pos = (
                            x * tile_width + tile_width / 2,
                            y * tile_height / 4 * 3 + tile_height / 2,
                        )
                    else:
                        pos = (
                            x * tile_width + tile_width,
                            y * tile_height / 4 * 3 + tile_height / 2,
                        )
                    Tile(surf=surf, pos=pos, group=self.tiles_group)

    def __str__(self):
        for layer in self.tmx.layers:
            print(layer)
        return ""


class Mini_map:
    def __init__(self, Szerokosc, Wysokosc, color, pos):
        self.Wysokosc = Wysokosc
        self.Szerokosc = Szerokosc
        self.origin = pos
        self.mapSurf = pygame.Surface((self.Szerokosc, self.Wysokosc))
        self.color = color
        self.mapSurf.fill(self.color)
        self.mapRect = self.mapSurf.get_frect(topright=pos)

    def fill(self):
        self.mapSurf.fill(self.color)
