import pygame
from projekt.ustawienia import *
from os.path import join
from projekt.narzedzia import Singleton
from .mapa import Mapa
from projekt.network import Client
from projekt.assetMenager import AssetManager


class Mini_map(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.mini_width = Mapa().Mapa_width / skala
        self.mini_height = Mapa().Mapa_height / skala
        self.surf = pygame.Surface((self.mini_width, self.mini_height))
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
        self.surf.fill((20, 20, 20))

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.mapRect.collidepoint(mouse_pos):
                pos_y = mouse_pos[1] - mini_map_pos[1]
                pos_x = mouse_pos[0] + self.mini_width - mini_map_pos[0]
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
                if Mapa().widziane[tile.x][tile.y]:
                    self.rysuj(tile)
                    if not tile.budynek is None:
                        self.draw_budynek(tile.budynek)
                if Mapa().widok[tile.x][tile.y] >= 0:
                    if not tile.jednostka is None:
                        self.draw_squad(tile.jednostka.color, tile.pos)
                elif Mapa().widziane[tile.x][tile.y]:
                    self.rysujChmure(tile)
        pygame.draw.rect(self.surf, mini_map_rect_color, self.rect, width=1)
        pygame.draw.rect(screen, "grey", self.mapRect, width=5)
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

    def rysujChmure(self, obiekt):
        pos = obiekt.pos
        pos = (pos[0] / skala, pos[1] / skala)
        image = pygame.transform.scale_by(
            AssetManager.get_asset("chmura"), 1.11111111 / skala
        )
        rect = image.get_frect(center=pos)
        self.surf.blit(image, rect)

    def draw_budynek(self, budynek):
        pos = budynek.pos
        pos = (pos[0] / skala, pos[1] / skala)
        image = pygame.transform.scale_by(budynek.image, 1.11111111 / skala)
        rect = image.get_frect(center=pos)
        w = tile_width / 2 / skala
        h = tile_height / 2 / skala
        hp = 54 / 2 / skala
        self.surf.blit(image, rect)
        pygame.draw.circle(self.surf, budynek.color, pos, w, width=1)
        # pygame.draw.polygon(
        # self.surf,
        # budynek.color,
        # [
        # (pos[0] - w, pos[1] - hp),
        # (pos[0] - w, pos[1] + hp),
        # (pos[0], pos[1] - h),
        # (pos[0] + w, pos[1] - hp),
        # (pos[0] + w, pos[1] + hp),
        # (pos[0], pos[1] + h),
        # ],
        # width=2,
        # )
