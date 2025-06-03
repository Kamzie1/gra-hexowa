import pygame
from projekt.ustawienia import *
from pytmx.util_pygame import load_pygame
from os.path import join
from .tile import Tile
from .budynek import Budynek
from projekt.narzedzia import *


class Mapa:
    sasiedzi1x = [-1, 0, 0, 1, 1, 1]

    sasiedzi1y = [0, 1, -1, 0, 1, -1]

    sasiedzi2x = [1, 0, 0, -1, -1, -1]

    sasiedzi2y = [0, 1, -1, 0, 1, -1]

    def __init__(self):
        self.origin = map_original_pos
        self.origin1 = None
        self.mapSurf = pygame.Surface((Mapa_width, Mapa_height))
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)
        self.tmx = load_pygame(join(folder_grafiki, plik_mapy))
        self.tiles_group = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.Tile_array = [
            [None for _ in range(map_tile_height)] for _ in range(map_tile_width)
        ]
        self.load_tiles()

    def update(self) -> None:
        if pygame.mouse.get_pos()[0] <= 0 + mouse_boundry_offset_x:
            self.origin1 = (self.origin[0] + mouse_border_speed, self.origin[1])
        elif pygame.mouse.get_pos()[0] >= Width - mouse_boundry_offset_x:
            self.origin1 = (self.origin[0] - mouse_border_speed, self.origin[1])
        elif pygame.mouse.get_pos()[1] <= 0 + mouse_boundry_offset_y:
            self.origin1 = (self.origin[0], self.origin[1] + mouse_border_speed)
        elif pygame.mouse.get_pos()[1] >= Height - mouse_boundry_offset_y:
            self.origin1 = (self.origin[0], self.origin[1] - mouse_border_speed)
        else:
            self.origin1 = None

        if not self.origin1 is None:
            if self.validateOffset((0, 0), self.origin1):
                self.origin = self.origin1
                self.mapRect = self.mapSurf.get_frect(topleft=self.origin)

        if pygame.mouse.get_pressed()[1]:
            # aktualizacja pozycji mapy względem ekranu
            self.update_pos()
        elif not pygame.mouse.get_pressed()[1]:
            self.original_origin = self.origin
            self.original_mouse_pos = pygame.mouse.get_pos()

    def update_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        offset = (
            mouse_pos[0] - self.original_mouse_pos[0],  # type: ignore (mój pylance świruje, więc to wyłącza podświetlenie błędu)
            mouse_pos[1] - self.original_mouse_pos[1],  # type: ignore
        )
        if self.validateOffset(offset, self.original_origin):
            self.origin = (
                self.original_origin[0] + offset[0],  # type: ignore
                self.original_origin[1] + offset[1],  # type: ignore
            )
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)

    def validateOffset(self, offset, original_origin) -> bool:
        # sprawdza, czy nie wychodzisz poza mapę
        if original_origin[0] + offset[0] > mapa_x_offset:
            return False
        if original_origin[0] + offset[0] + Mapa_width < Width - mapa_x_offset:
            return False
        if original_origin[1] + offset[1] > mapa_y_offset:
            return False
        if original_origin[1] + offset[1] + Mapa_height < Height - mapa_y_offset:
            return False
        return True

    def load_tiles(self):
        # loaduje z tmx tilesy i przypisuje je do grupy
        for layer in self.tmx.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer.iter_data():
                    pos = oblicz_pos(x, y)
                    props = self.tmx.get_tile_properties_by_gid(gid)
                    image = self.tmx.get_tile_image_by_gid(gid)
                    if x == pos_rec_x and y == pos_rec_y:
                        budynek = Budynek(pos, self.building_group, budynek_img)
                        tile = Tile(
                            surf=image,
                            pos=pos,
                            x=x,
                            y=y,
                            group=self.tiles_group,
                            id=x + 30 * y,
                            budynek=budynek,
                            koszt_ruchu=props["koszt_ruchu"],
                            typ=props["id"],
                        )
                    else:
                        tile = Tile(
                            surf=image,
                            x=x,
                            y=y,
                            pos=pos,
                            group=self.tiles_group,
                            id=x + 30 * y,
                            koszt_ruchu=props["koszt_ruchu"],
                            typ=props["id"],
                        )
                    self.Tile_array[x][y] = tile

    def possible_moves(self, x, y, ruch):
        tablica_odwiedzonych = [
            [0 for _ in range(map_tile_width)] for _ in range(map_tile_height)
        ]
        tablica_odwiedzonych[x][y] = 1
        queue = priority_queue()
        queue.append((x, y, ruch))
        while not queue.empty():
            x, y, ruch = queue.pop()
            match (y % 2):
                case 1:
                    sasiedzix = Mapa.sasiedzi1x
                    sasiedziy = Mapa.sasiedzi1y
                case 0:
                    sasiedzix = Mapa.sasiedzi2x
                    sasiedziy = Mapa.sasiedzi2y
            for i in range(6):
                if x + sasiedzix[i] >= map_tile_width or x + sasiedzix[i] < 0:
                    continue
                if y + sasiedziy[i] >= map_tile_height or y + sasiedziy[i] < 0:
                    continue
                if tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] == 1:
                    continue
                if (
                    ruch
                    - self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].koszt_ruchu
                    < 0
                ):
                    continue
                tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] = 1
                queue.append(
                    (
                        x + sasiedzix[i],
                        y + sasiedziy[i],
                        ruch
                        - self.Tile_array[x + sasiedzix[i]][
                            y + sasiedziy[i]
                        ].koszt_ruchu,
                    )
                )
        return tablica_odwiedzonych

    def __str__(self):
        for layer in self.tmx.layers:
            print(layer)
        return ""


class Mini_map:
    def __init__(self):
        self.origin = mini_map_pos
        self.image = pygame.image.load(join(folder_grafiki, minimapa_image)).convert()
        self.scaledSurf = pygame.transform.smoothscale(
            self.image, (mini_width, mini_height)
        )
        self.surf = self.scaledSurf
        self.mapRect = self.surf.get_frect(topright=mini_map_pos)

        self.origin = map_original_pos
        self.rectsurf = pygame.Surface(
            (mini_map_mouse_rect_width, mini_map_mouse_rect_height)
        )
        self.rect = self.rectsurf.get_frect(topleft=self.origin)

    def update(self):
        self.surf = self.scaledSurf.copy()

    def update_minimap(self, mapa):
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
