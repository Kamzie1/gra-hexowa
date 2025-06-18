import pygame
from projekt.ustawienia import *
from pytmx.util_pygame import load_pygame
from os.path import join
from .tile import Tile, Ruch, Najechanie, Klikniecie, Podswietlenie
from .budynek import Budynek
from projekt.narzedzia import *
from projekt.jednostki import Wojownik, Squad


class Mapa:
    sasiedzi1x = [-1, 0, 0, 1, 1, 1]

    sasiedzi1y = [0, 1, -1, 0, 1, -1]

    sasiedzi2x = [1, 0, 0, -1, -1, -1]

    sasiedzi2y = [0, 1, -1, 0, 1, -1]

    def __init__(self, miasto_pos, miasto_x, miasto_y, player, opponent, state):
        self._origin = (-miasto_pos[0] + srodek[0], -miasto_pos[1] + srodek[1])
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
        self.move_group = pygame.sprite.Group()
        self.move_flag = None
        self.correct_moves = None
        self.army_group = pygame.sprite.Group()
        self.podswietlenie_group = pygame.sprite.Group()

        self.player = player
        self.opponent = opponent

        self.najechanie = Najechanie(
            pygame.image.load(
                join("Grafika/tile-grafika", "Hex_najechanie.png")
            ).convert_alpha(),
            (tile_width / 2, tile_height / 2),
            pygame.image.load(
                join("Grafika/tile-grafika", f"{player.color}_podswietlenie.png")
            ).convert_alpha(),
            pygame.image.load(
                join("Grafika/tile-grafika", f"{opponent.color}_podswietlenie.png")
            ).convert_alpha(),
        )
        self.klikniecie = Klikniecie(
            pygame.image.load(
                join("Grafika/tile-grafika", "hex-klikniecie.png")
            ).convert_alpha(),
            (tile_width / 2, tile_height / 2),
        )
        self.import_state(state)

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
        self.najechanie.update(
            mouse_pos, self.Tile_array, self.origin, self.player.id, self.opponent.id
        )

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

    def load_tiles(self):
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
        self.podswietlenie_group.draw(self.mapSurf)
        self.mapSurf.blit(
            self.najechanie.surf[self.najechanie.flag], self.najechanie.rect
        )
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
                                    join(
                                        f"{folder_grafiki}/tile-grafika",
                                        "hex-klikniecie.png",
                                    )
                                ).convert_alpha(),
                                (tile.pos),
                                self.correct_moves[tile.x][tile.y],
                            )
            self.move_group.draw(self.mapSurf)

    def event(self, mouse_pos, flag, turn, id):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, self.origin)

        for tiles in self.Tile_array:
            for tile in tiles:
                if clicked(tile.pos, mouse_pos):
                    flag.klikniecie_flag = True
                    self.klikniecie.origin = tile.pos
                    if not turn % 2 == id:
                        return
                    if self.move_flag is None:
                        self.move_flag = tile.jednostka
                        if not self.move_flag is None and tile.jednostka.owner == id:
                            self.correct_moves = self.possible_moves(
                                tile.x, tile.y, self.move_flag
                            )
                        else:
                            self.move_flag = None

                    else:
                        if (
                            tile.jednostka is None
                            and self.correct_moves[tile.x][tile.y] >= 0
                        ):
                            if not self.move_flag.tile is None:
                                self.move(tile, flag)
                            else:
                                self.recruit(tile, flag)
                        self.move_flag = None
                        for tile in self.move_group:
                            tile.kill()

    def move(self, tile, flag):
        self.move_flag.tile.jednostka = None
        self.move_flag.pos = tile.pos
        self.move_flag.tile = tile
        self.move_flag.ruch = self.correct_moves[tile.x][tile.y]
        tile.jednostka = self.move_flag
        flag.klikniecie_flag = False

    def recruit(self, tile, flag):
        try:
            self.player.gold -= self.player.frakcja["jednostka"][
                self.move_flag.wojownicy[0].id
            ]["cost"]
        except:
            print("not enough money")
        else:
            self.move_flag.pos = tile.pos
            self.move_flag.tile = tile
            self.move_flag.ruch = self.correct_moves[tile.x][tile.y]
            tile.jednostka = self.move_flag
            flag.klikniecie_flag = False

    def load_state(self):
        state = {}
        state["jednostka"] = []
        state["budynek"] = []
        for tiles in self.Tile_array:
            for tile in tiles:
                if not tile.jednostka is None:
                    state["jednostka"].append(tile.jednostka.get_data())
                if not tile.budynek is None:
                    stan_budynku = {
                        "owner": tile.budynek.owner,
                        "pos": tile.budynek.pos,
                        "color": tile.budynek.color,
                        "id": tile.budynek.id,
                        "zdrowie": tile.budynek.zdrowie,
                        "morale": tile.budynek.morale,
                    }
                    state["budynek"].append(stan_budynku)
        return state

    def get_tile(self, pos):
        for tiles in self.Tile_array:
            for tile in tiles:
                if tile.pos == tuple(pos):
                    return tile
        return None

    def import_state(self, state):
        for jednostka in self.building_group:
            jednostka.kill()

        for jednostka in self.podswietlenie_group:
            jednostka.kill()

        self.army_group.empty()
        self.building_group.empty()
        self.podswietlenie_group.empty()

        for tiles in self.Tile_array:
            for tile in tiles:
                tile.jednostka = None
                tile.budynek = None

        for jednostka in state["jednostka"]:
            tile = self.get_tile(jednostka["pos"])
            if jednostka["owner"] == self.player.id:
                frakcja = self.player.frakcja
            else:
                frakcja = self.opponent.frakcja
            s = Squad(self.army_group, jednostka, tile, frakcja)
            tile.jednostka = s

        for budynek in state["budynek"]:
            tile = self.get_tile(budynek["pos"])
            if budynek["owner"] == self.player.id:
                frakcja = self.player.frakcja
                color = self.player.color

            else:
                frakcja = self.opponent.frakcja
                color = self.opponent.color
            b = Budynek(
                frakcja[budynek["id"]],
                budynek["id"],
                budynek["pos"],
                self.building_group,
                budynek["owner"],
                budynek["color"],
                budynek["zdrowie"],
                budynek["morale"],
            )
            Podswietlenie(
                f"{color}_podswietlenie.png", tile.pos, self.podswietlenie_group
            )
            tile.budynek = b

    def zarabiaj(self):
        for budynek in self.building_group:
            if isinstance(budynek, Budynek):
                budynek.zarabiaj(self.player)
            else:
                print("to nie budynek")

    def heal(self):
        for budynek in self.building_group:
            tile = self.get_tile(budynek.pos)
            if not tile.jednostka is None:
                tile.jednostka.heal(budynek.heal)

    def __str__(self):
        for layer in self.tmx.layers:
            print(layer)
        return ""
