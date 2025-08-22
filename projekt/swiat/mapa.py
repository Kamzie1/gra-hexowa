import pygame
from projekt.ustawienia import *
from pytmx.util_pygame import load_pygame
from os.path import join
from .tile import Tile, Ruch, Najechanie, Klikniecie
from projekt.narzedzia import (
    oblicz_pos,
    get_sasiedzi,
    Queue,
    priority_queue,
    pozycja_myszy_na_surface,
    clicked,
    id_to_pos,
)
from projekt.jednostki import Squad, Miasto, Wioska
from projekt.assetMenager import AssetManager
from projekt.narzedzia import Singleton, AttackDisplay
from projekt.network import Client
from .squadDisplay import SquadDisplay
from projekt.flag import Flag


class Mapa(metaclass=Singleton):
    def __init__(self, czywidzi):
        if hasattr(self, "_initialized"):
            return
        self._origin = (
            -Client().player.pos[0] + srodek[0],
            -Client().player.pos[1] + srodek[1],
        )
        self.origin1 = None
        self.width, self.height = Client().width, Client().height
        self.Mapa_width, self.Mapa_height = oblicz_pos(Client().width, Client().height)
        self.mapSurf = pygame.Surface((self.Mapa_width, self.Mapa_height))
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)
        self.mapa = Client().map
        self.tiles_group = pygame.sprite.Group()
        self.building_group = pygame.sprite.Group()
        self.Tile_array = [
            [None for _ in range(Client().width)] for _ in range(Client().height)
        ]
        self.widok = [
            [czywidzi - 1 for _ in range(Client().width)]
            for _ in range(Client().height)
        ]
        self.widziane = [
            [czywidzi for _ in range(Client().width)] for _ in range(Client().height)
        ]
        self.load_tiles()
        self.move_group = pygame.sprite.Group()
        self.move_flag = None
        self.correct_moves = None
        self.army_group = pygame.sprite.Group()
        self.widok_group = pygame.sprite.Group()
        self.czywidzi = czywidzi

        self.split = None

        self.najechanie = Najechanie(
            (tile_width / 2, tile_height / 2),
        )
        self.klikniecie = Klikniecie(
            AssetManager.get_asset("hex-klikniecie (2)"),
            (tile_width / 2, tile_height / 2),
        )
        self.import_state(Client().state, Client().users)
        self.calculate_widok()

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
            mouse_pos,
            self.Tile_array,
            self.origin,
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
        if original_origin[0] + offset[0] + self.Mapa_width < Width - mapa_x_offset:
            return False
        if original_origin[1] + offset[1] > mapa_y_offset:
            return False
        if original_origin[1] + offset[1] + self.Mapa_height < Height - mapa_y_offset:
            return False
        return True

    def load_tiles(self):
        x: int = 0
        y: int = 0
        for row in self.mapa:
            for ident in row:
                pos = oblicz_pos(x, y)
                props = AssetManager.get_tiles_property(ident - 1)
                tile = Tile(
                    x=x,
                    y=y,
                    pos=pos,
                    group=self.tiles_group,
                    id=x + 30 * y,
                    koszt_ruchu=props["koszt_ruchu"],
                    typ=props["typ"],
                    image=props["image"],
                    obrona=props["obrona"],
                    widocznosc=props["widocznosc"],
                )

                self.Tile_array[int(x)][y] = tile
                x += 1
                x %= self.width
            y += 1

    def BFS(self, x1, y1, x2, y2):
        tablica_odwiedzonych = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        tablica_odwiedzonych[x1][y1] = 1
        queue = Queue()
        queue.append((x1, y1))
        while not queue.empty():
            x, y = queue.pop()
            sasiedzix, sasiedziy = get_sasiedzi(x, y)
            for i in range(6):
                if x + sasiedzix[i] >= self.width or x + sasiedzix[i] < 0:
                    continue
                if y + sasiedziy[i] >= self.height or y + sasiedziy[i] < 0:
                    continue
                if tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] > 0:
                    continue

                tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] = (
                    tablica_odwiedzonych[x][y] + 1
                )

                if x + sasiedzix[i] == x2 and y + sasiedziy[i] == y2:
                    return tablica_odwiedzonych[x2][y2]
                queue.append(
                    (
                        x + sasiedzix[i],
                        y + sasiedziy[i],
                    )
                )
        return -1

    def possible_moves(self, x, y, jednostka):
        tablica_odwiedzonych = [
            [-1 for _ in range(self.width)] for _ in range(self.height)
        ]
        tablica_odwiedzonych[x][y] = jednostka.ruch
        queue = priority_queue()
        if jednostka.ruch == jednostka.max_ruch:
            queue.append(
                (x, y, jednostka.ruch + Client().player.akcje["movement_rozkaz"])
            )
        else:
            queue.append((x, y, jednostka.ruch))
        while not queue.empty():
            x, y, ruch = queue.pop()
            sasiedzix, sasiedziy = get_sasiedzi(x, y)
            for i in range(6):
                if x + sasiedzix[i] >= self.width or x + sasiedzix[i] < 0:
                    continue
                if y + sasiedziy[i] >= self.height or y + sasiedziy[i] < 0:
                    continue
                if tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] >= 0:
                    continue
                if (
                    self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].budynek
                    is not None
                ):
                    if (
                        ruch
                        - self.Tile_array[x + sasiedzix[i]][
                            y + sasiedziy[i]
                        ].budynek.koszt_ruchu
                        < 0
                    ):
                        continue
                    tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] = (
                        ruch
                        - self.Tile_array[x + sasiedzix[i]][
                            y + sasiedziy[i]
                        ].budynek.koszt_ruchu
                    )
                    queue.append(
                        (
                            x + sasiedzix[i],
                            y + sasiedziy[i],
                            ruch
                            - self.Tile_array[x + sasiedzix[i]][
                                y + sasiedziy[i]
                            ].budynek.koszt_ruchu,
                        )
                    )
                else:
                    if (
                        ruch
                        - self.Tile_array[x + sasiedzix[i]][
                            y + sasiedziy[i]
                        ].koszt_ruchu
                        < 0
                    ):
                        continue
                    tablica_odwiedzonych[x + sasiedzix[i]][y + sasiedziy[i]] = (
                        ruch
                        - self.Tile_array[x + sasiedzix[i]][
                            y + sasiedziy[i]
                        ].koszt_ruchu
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

    def widok_jednostka(self, x, y, jednostka):
        self.widziane[x][y] = True
        self.widok[x][y] = jednostka.wzrok
        queue = priority_queue()
        queue.append((x, y, jednostka.wzrok))
        while not queue.empty():
            x, y, wzrok = queue.pop()
            sasiedzix, sasiedziy = get_sasiedzi(x, y)
            for i in range(6):
                if x + sasiedzix[i] >= self.width or x + sasiedzix[i] < 0:
                    continue
                if y + sasiedziy[i] >= self.height or y + sasiedziy[i] < 0:
                    continue
                if (
                    self.widok[x + sasiedzix[i]][y + sasiedziy[i]]
                    > wzrok
                    - self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].widocznosc
                ):
                    continue
                if (
                    wzrok
                    - self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].widocznosc
                    < 0
                ):
                    continue
                self.widok[x + sasiedzix[i]][y + sasiedziy[i]] = (
                    wzrok
                    - self.Tile_array[x + sasiedzix[i]][y + sasiedziy[i]].widocznosc
                )
                self.widziane[x + sasiedzix[i]][y + sasiedziy[i]] = True
                queue.append(
                    (
                        x + sasiedzix[i],
                        y + sasiedziy[i],
                        wzrok
                        - self.Tile_array[x + sasiedzix[i]][
                            y + sasiedziy[i]
                        ].widocznosc,
                    )
                )

    def calculate_widok(self):
        self.widok = [
            [self.czywidzi - 1 for _ in range(self.width)] for _ in range(self.height)
        ]
        for jednostka in self.army_group:
            if jednostka.owner_id == Client().player.id and jednostka.tile is not None:
                self.widok_jednostka(jednostka.tile.x, jednostka.tile.y, jednostka)

    def draw(self, screen):
        self.mapSurf.fill("black")
        for tile in self.tiles_group:
            if self.widziane[tile.x][tile.y]:
                tile.draw(self.mapSurf)
                if self.widok[tile.x][tile.y] == -1:
                    self.mapSurf.blit(AssetManager.get_asset("chmura"), tile.rect)

        for budynek in self.building_group:
            if (
                budynek.tile is not None
                and self.widziane[budynek.tile.x][budynek.tile.y] > 0
            ):
                budynek.draw(self.mapSurf)
        self.najechanie.draw(self.mapSurf)
        if Flag().klikniecie_flag:
            self.mapSurf.blit(self.klikniecie.image, self.klikniecie.rect)
        if not self.move_flag is None:
            if len(self.move_group) == 0:
                for tiles in self.Tile_array:
                    for tile in tiles:
                        if (
                            not self.correct_moves is None
                            and self.correct_moves[tile.x][tile.y] >= 0
                        ):
                            Ruch(
                                self.move_group,
                                AssetManager.get_asset("hex-klikniecie (2)"),
                                (tile.pos),
                                self.correct_moves[tile.x][tile.y],
                            )
            self.move_group.draw(self.mapSurf)
        for jednostka in self.army_group:
            if (
                jednostka.tile is not None
                and self.widok[jednostka.tile.x][jednostka.tile.y] >= 0
            ):
                jednostka.draw(self.mapSurf)
        screen.blit(self.mapSurf, self.mapRect)

    def event(
        self,
        mouse_pos,
        squadButtonDisplay,
        rotateButton,
    ):
        failed = False
        if AttackDisplay().show:
            if AttackDisplay().rect.collidepoint(mouse_pos):
                AttackDisplay().event(mouse_pos)
                return

        if SquadDisplay().show:
            if SquadDisplay().rect.collidepoint(mouse_pos):
                return

        if not self.move_flag is None:
            if squadButtonDisplay.rect.collidepoint(mouse_pos):
                return
            if rotateButton.rect.collidepoint(mouse_pos):
                return

        mouse_pos = pozycja_myszy_na_surface(mouse_pos, self.origin)
        for tiles in self.Tile_array:
            for tile in tiles:
                if clicked(tile.pos, mouse_pos):
                    AttackDisplay().show = False
                    Flag().klikniecie_flag = True
                    self.klikniecie.origin = tile.pos

                    if self.move_flag is None:
                        self.move_flag = tile.jednostka
                        if (
                            not self.move_flag is None
                            and tile.jednostka.owner_id == Client().player.id
                            and Client().turn % len(Client().users)
                            == Client().player.id
                        ):
                            self.correct_moves = self.possible_moves(
                                tile.x, tile.y, self.move_flag
                            )

                    else:
                        if (
                            not self.correct_moves is None
                            and self.correct_moves[tile.x][tile.y] >= 0
                        ):
                            if self.move_flag.tile is None:
                                if tile.jednostka is None:
                                    self.recruit(tile)
                                elif tile.jednostka.owner_id == Client().player.id:
                                    self.recruit_join(tile)
                                elif tile.jednostka.owner_id == Client().opponent.id:
                                    pass
                            elif tile.jednostka is None:
                                self.move(tile)
                            else:
                                if tile.jednostka.owner_id == Client().player.id:
                                    if not self.move_flag.tile == tile:
                                        try:
                                            self.join(
                                                tile.jednostka, self.move_flag, tile
                                            )
                                        except:
                                            pass
                                elif tile.jednostka.owner_id != Client().player.id:
                                    distance = self.attackValidate(
                                        self.move_flag, tile.jednostka
                                    )
                                    if distance:
                                        AttackDisplay().update(
                                            self.move_flag,
                                            tile.jednostka,
                                            distance,
                                            self.move_flag.tile.x,
                                            self.move_flag.tile.y,
                                            tile.x,
                                            tile.y,
                                            tile.obrona,
                                        )
                        else:
                            if (
                                not tile.jednostka is None
                                and Client().turn % len(Client().users) == id
                            ):
                                if (
                                    tile.jednostka.owner_id != Client().player.id
                                    and self.move_flag.owner_id == Client().player.id
                                ):
                                    distance = self.attackValidate(
                                        self.move_flag, tile.jednostka
                                    )
                                    if distance:
                                        AttackDisplay().update(
                                            self.move_flag,
                                            tile.jednostka,
                                            distance,
                                            self.move_flag.tile.x,
                                            self.move_flag.tile.y,
                                            tile.x,
                                            tile.y,
                                            tile.obrona,
                                        )
                                    else:
                                        failed = True
                                else:
                                    failed = True
                            else:
                                failed = True
                        Flag().klikniecie_flag = False
                        if self.split is not None and failed:
                            self.move_flag.kill()
                        self.move_flag = None
                        SquadDisplay().show = False
                        self.correct_moves = None
                        self.split = None
                        for tile in self.move_group:
                            tile.kill()

    def move(self, tile):
        if self.split is None:
            self.move_flag.tile.jednostka = None
        else:
            self.move_flag.tile.jednostka.wojownicy[self.split] = None
            print(self.move_flag.tile.jednostka)
        self.move_flag.pos = tile.pos
        self.move_flag.tile = tile
        self.move_flag.ruch = self.correct_moves[tile.x][tile.y]
        tile.jednostka = self.move_flag
        if tile.budynek is not None:
            print("owning...")
            tile.budynek.own(
                self.move_flag.owner,
                self.move_flag.owner_id,
                self.move_flag.color,
            )
        self.calculate_widok()
        self.calculate_income()

    def recruit(self, tile):
        try:
            Client().player.gold -= Client().player.frakcja["jednostka"][
                self.move_flag.wojownicy[3].id
            ]["cost"]
        except:
            print("not enough money")
        else:
            self.move_flag.pos = tile.pos
            self.move_flag.tile = tile
            self.move_flag.ruch = self.correct_moves[tile.x][tile.y]
            tile.jednostka = self.move_flag

    def recruit_join(self, tile):
        try:
            Client().player.gold -= Client().player.frakcja["jednostka"][
                self.move_flag.wojownicy[3].id
            ]["cost"]
        except:
            print("not enough money")
        else:
            try:
                self.join(tile.jednostka, self.move_flag, tile)
            except:
                pass

    def join(self, squad1, squad2, tile):
        if not self.validate_join(squad1, squad2):
            raise ValueError

        squad2.ruch = self.correct_moves[tile.x][tile.y]

        squad1 = squad1 + squad2

        if not squad2.tile is None:
            squad2.tile.jednostka = None
        squad2.kill()

    def validate_join(self, squad1, squad2):
        none_count = 0
        not_none_count = 0
        for wojownik in squad1.wojownicy:
            if wojownik is None:
                none_count += 1
        for wojownik in squad2.wojownicy:
            if wojownik is not None:
                not_none_count += 1
        if 7 - none_count + not_none_count > 7:
            return False
        return True

    def attackValidate(self, squad1, squad2):
        distance = self.BFS(squad1.tile.x, squad1.tile.y, squad2.tile.x, squad2.tile.y)
        if distance - 1 > squad1.range:
            return 0
        return distance - 1

    def load_state(self):
        state = {}
        state["jednostki"] = []
        state["budynki"] = []
        for tiles in self.Tile_array:
            for tile in tiles:
                if not tile.jednostka is None:
                    state["jednostki"].append(tile.jednostka.get_data())
                if not tile.budynek is None:
                    stan_budynku = {
                        "owner": tile.budynek.owner,
                        "owner_id": tile.budynek.owner_id,
                        "pos": tile.budynek.pos,
                        "color": tile.budynek.color,
                        "id": tile.budynek.id,
                    }
                    state["budynki"].append(stan_budynku)
        return state

    def get_tile(self, pos):
        for tiles in self.Tile_array:
            for tile in tiles:
                if tile.pos == tuple(pos):
                    return tile
        return None

    def import_state(self, state, users):
        self.army_group.empty()
        self.building_group.empty()

        for tiles in self.Tile_array:
            for tile in tiles:
                tile.jednostka = None
                tile.budynek = None

        for jednostka in state["jednostki"]:
            tile = self.get_tile(jednostka["pos"])
            frakcja = AssetManager.frakcja[
                Client().users[jednostka["owner_id"]]["fraction"]
            ]
            s = Squad(self.army_group, jednostka, tile, frakcja)
            tile.jednostka = s

        for budynek in state["budynki"]:
            tile = self.get_tile(budynek["pos"])
            frakcja = AssetManager.frakcja[
                Client().users[budynek["owner_id"]]["fraction"]
            ]
            if budynek["id"] == 0:
                b = Miasto(
                    self.building_group,
                    budynek,
                    tile,
                    frakcja,
                )
                tile.obrona = AssetManager.get_mnoznik(
                    "mury_upgrade", Client().player.akcje["mury_upgrade"]
                )  # dodać dla przeciwnika !!!

            else:
                b = Wioska(
                    self.building_group,
                    budynek,
                    tile,
                    frakcja,
                )
                tile.obrona = b.budynek["obrona"]
            tile.koszt_ruchu = b.budynek["ruch"]
            tile.budynek = b

        self.calculate_income()

    def refresh(self):
        for budynek in self.building_group:
            budynek.tile.obrona = AssetManager.get_mnoznik(
                "mury_upgrade", Client().player.akcje["mury_upgrade"]
            )

    def calculate_income(self):
        Client().player.zloto_income = 0
        for budynek in self.building_group:
            if isinstance(budynek, Miasto) and budynek.owner_id == Client().player.id:
                Client().player.zloto_income += int(
                    budynek.earn["gold"]
                    * AssetManager.get_mnoznik(
                        "zloto_upgrade", Client().player.akcje["zloto_upgrade"]
                    )
                    * Client().player.akcje["zloto_rozkaz"]
                )
            else:
                pass

    def heal(self):
        for budynek in self.building_group:
            if isinstance(budynek, Miasto):
                if budynek.owner_id == Client().player.id:
                    tile = budynek.tile
                    if (
                        not tile.jednostka is None
                        and tile.jednostka.owner_id == budynek.owner_id
                    ):
                        tile.jednostka.heal(budynek.heal)
            else:
                pass

    def __str__(self):
        for layer in self.tmx.layers:
            print(layer)
        return ""
