import pygame
from projekt.ustawienia import *
from pytmx.util_pygame import load_pygame
from os.path import join
from .tile import Tile, Ruch, Najechanie
from .budynek import Budynek
from projekt.narzedzia import *


class Mapa:
    sasiedzi1x = [-1, 0, 0, 1, 1, 1]

    sasiedzi1y = [0, 1, -1, 0, 1, -1]

    sasiedzi2x = [1, 0, 0, -1, -1, -1]

    sasiedzi2y = [0, 1, -1, 0, 1, -1]

    def __init__(self, miasto_pos, miasto_x, miasto_y):
        self._origin = map_original_pos
        self.origin1 = None
        self.mapSurf = pygame.Surface((Mapa_width, Mapa_height))
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)
        self.tmx = load_pygame(join(folder_grafiki, plik_mapy))
        self.tiles_group = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.Tile_array = [
            [None for _ in range(map_tile_height)] for _ in range(map_tile_width)
        ]
        self.load_tiles(miasto_pos, miasto_x, miasto_y)
        self.move_group = pygame.sprite.Group()
        self.move_flag = None
        self.correct_moves = None
        self.najechanie = Najechanie(
            pygame.image.load(
                join("grafika/tile-grafika", "Hex_najechanie.png")
            ).convert_alpha(),
            (tile_width / 2, tile_height / 2),
            pygame.image.load(
                join("grafika/tile-grafika", "Hex_wrogie_podswietlanie.png")
            ).convert_alpha(),
        )
        self.klikniecie = Najechanie(
            pygame.image.load(
                join("grafika/tile-grafika", "Hex-klikniecie.png")
            ).convert_alpha(),
            (tile_width / 2, tile_height / 2),
            pygame.image.load(
                join("grafika/tile-grafika", "Hex_wrogie_podswietlanie.png")
            ).convert_alpha(),
        )

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        self.update_based_border(mouse_pos)
        self.update_based_mouse(mouse_pos)
        self.najechanie.update(mouse_pos, self.Tile_array, self.origin)

    def update_based_mouse(self, mouse_pos):
        if pygame.mouse.get_pressed()[1]:
            self.update_pos(mouse_pos)
        else:
            self.original_origin = self.origin
            self.original_mouse_pos = mouse_pos

    def update_pos(self, mouse_pos):
        offset = (
            mouse_pos[0] - self.original_mouse_pos[0],
            mouse_pos[1] - self.original_mouse_pos[1],
        )
        if self.validateOffset(offset, self.original_origin):
            self.origin = (
                self.original_origin[0] + offset[0],
                self.original_origin[1] + offset[1],
            )

    def update_based_border(self, mouse_pos):
        if mouse_pos[0] <= 0 + mouse_boundry_offset_x:
            self.origin1 = (self.origin[0] + mouse_border_speed, self.origin[1])
        elif mouse_pos[0] >= Width - mouse_boundry_offset_x:
            self.origin1 = (self.origin[0] - mouse_border_speed, self.origin[1])
        elif mouse_pos[1] <= 0 + mouse_boundry_offset_y:
            self.origin1 = (self.origin[0], self.origin[1] + mouse_border_speed)
        elif mouse_pos[1] >= Height - mouse_boundry_offset_y:
            self.origin1 = (self.origin[0], self.origin[1] - mouse_border_speed)
        else:
            self.origin1 = None

        if not self.origin1 is None:
            if self.validateOffset((0, 0), self.origin1):
                self.origin = self.origin1

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

    def load_tiles(self, miasto_pos, miasto_x, miasto_y):
        # loaduje z tmx tilesy i przypisuje je do grupy
        for layer in self.tmx.visible_layers:
            if hasattr(layer, "data"):
                for x, y, gid in layer.iter_data():
                    pos = oblicz_pos(x, y)
                    props = self.tmx.get_tile_properties_by_gid(gid)
                    image = self.tmx.get_tile_image_by_gid(gid)
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
                    if x == miasto_x and y == miasto_y:
                        budynek = Budynek(miasto_pos, self.building_group, budynek_img)
                        tile.budynek = budynek

                    self.Tile_array[x][y] = tile

    def possible_moves(self, x, y, jednostka):
        tablica_odwiedzonych = [
            [-1 for _ in range(map_tile_width)] for _ in range(map_tile_height)
        ]
        tablica_odwiedzonych[x][y] = jednostka.ruch
        queue = priority_queue()
        queue.append((x, y, jednostka.ruch))
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
                if tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] >= 0:
                    continue
                if (
                    ruch
                    - self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].koszt_ruchu
                    < 0
                ):
                    continue
                tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] = (
                    ruch
                    - self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].koszt_ruchu
                )
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

    def draw(self, screen, flag):
        screen.blit(self.mapSurf, self.mapRect)  # rysuje mapę
        self.tiles_group.draw(self.mapSurf)  # rysuje tilesy
        self.building_group.draw(self.mapSurf)  # rysuje budynki
        if self.najechanie.flag:
            self.mapSurf.blit(self.najechanie.image, self.najechanie.rect)
        else:
            self.mapSurf.blit(self.najechanie.image2, self.najechanie.rect)
        if flag.klikniecie_flag:
            self.mapSurf.blit(self.klikniecie.image, self.klikniecie.rect)
        if not self.move_flag is None:
            if len(self.move_group) == 0:
                for tiles in self.Tile_array:
                    for tile in tiles:
                        if self.correct_moves[tile.x][tile.y] >= 0:
                            Ruch(
                                self.move_group,
                                pygame.image.load(
                                    join("grafika/tile-grafika", "Hex-klikniecie.png")
                                ).convert_alpha(),
                                (tile.pos),
                                self.correct_moves[tile.x][tile.y],
                            )
            self.move_group.draw(self.mapSurf)

    def event(self, mouse_pos, flag):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, self.origin)

        for tiles in self.Tile_array:
            for tile in tiles:
                if clicked(tile.pos, mouse_pos):
                    flag.klikniecie_flag = True
                    self.klikniecie.origin = tile.pos
                    if self.move_flag is None:
                        print("clicked")
                        self.move_flag = tile.jednostka
                        if not self.move_flag is None:
                            self.correct_moves = self.possible_moves(
                                tile.x, tile.y, self.move_flag
                            )

                    else:
                        if (
                            tile.jednostka is None
                            and self.correct_moves[tile.x][tile.y] >= 0
                        ):
                            print(self.correct_moves[tile.x][tile.y])
                            print("move")
                            self.move_flag.pos = tile.pos
                            self.move_flag.tile.jednostka = None
                            self.move_flag.tile = tile
                            self.move_flag.ruch = self.correct_moves[tile.x][tile.y]
                            tile.jednostka = self.move_flag
                            flag.klikniecie_flag = False

                        self.move_flag = None
                        for tile in self.move_group:
                            tile.kill()

    def __str__(self):
        for layer in self.tmx.layers:
            print(layer)
        return ""
