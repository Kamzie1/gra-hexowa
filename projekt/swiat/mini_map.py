import pygame
from projekt.ustawienia import *
from os.path import join


class Mini_map:
    def __init__(self):
        self.image = pygame.image.load(join(folder_grafiki, minimapa_image)).convert()
        self.scaledSurf = pygame.transform.smoothscale(
            self.image, (mini_width, mini_height)
        )
        self.surf = self.scaledSurf
        self.mapRect = self.surf.get_frect(topright=mini_map_pos)

        self._origin = map_original_pos
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
        self.surf = self.scaledSurf.copy()

    def update(self, mapa):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.mapRect.collidepoint(mouse_pos):
                # jeżeli zachodzi interakcja z mini mapą, to licz współrzędne (odpowiednio zeskalowane)
                pos_y = mouse_pos[1] - mini_map_pos[1]
                pos_x = mouse_pos[0] + mini_width - mini_map_pos[0]
                mapa_pos_y = pos_y * skala
                mapa_pos_x = pos_x * skala
                mapa.origin = (-mapa_pos_x + srodek[0], -mapa_pos_y + srodek[1])  # type: ignore , srodek wyrównuje widok, przenosi origin o połowę wektora przekątnej ekranu
                mapa.mapRect = mapa.mapSurf.get_frect(
                    topleft=mapa.origin  # zaktualizuj położenie mapy
                )

    def draw(self, screen, origin):
        self.refresh()
        self.origin = (
            -origin[0] / skala,
            -origin[1] / skala,
        )

        pygame.draw.rect(self.surf, mini_map_rect_color, self.rect, width=1)
        pygame.draw.rect(screen, (0, 0, 0), self.mapRect, width=2)  # rysuje border
        screen.blit(self.surf, self.mapRect)  # rysuje mini mapę
