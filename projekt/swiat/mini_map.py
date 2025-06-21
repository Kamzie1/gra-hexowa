import pygame
from projekt.ustawienia import *
from os.path import join


class Mini_map:
    def __init__(self, miasto_pos):
        self.surf = pygame.Surface((Mapa_width / skala, Mapa_height / skala))
        self.mapRect = self.surf.get_frect(topright=mini_map_pos)

        self._origin = (-miasto_pos[0] + srodek[0], -miasto_pos[0] + srodek[1])
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

    def update(self, mapa):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.mapRect.collidepoint(mouse_pos):
                pos_y = mouse_pos[1] - mini_map_pos[1]
                pos_x = mouse_pos[0] + mini_width - mini_map_pos[0]
                mapa_pos_y = pos_y * skala
                mapa_pos_x = pos_x * skala
                mapa.origin = (-mapa_pos_x + srodek[0], -mapa_pos_y + srodek[1])
                mapa.mapRect = mapa.mapSurf.get_frect(topleft=mapa.origin)

    def draw(self, screen, origin, Tile_array, widok):
        self.refresh()
        self.origin = (
            -origin[0] / skala,
            -origin[1] / skala,
        )
        for tiles in Tile_array:
            for tile in tiles:
                if widok[tile.x][tile.y] >= 0:
                    self.rysuj(tile)
                    if not tile.budynek is None:
                        self.draw_budynek(tile.budynek)
                    if not tile.jednostka is None:
                        self.draw_squad(tile.jednostka.color, tile.pos)
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
