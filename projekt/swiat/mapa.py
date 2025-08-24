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
)
from projekt.jednostki import Squad, Miasto, Wioska
from projekt.assetMenager import AssetManager
from projekt.narzedzia import Singleton, AttackDisplay
from projekt.network import Client
from .squadDisplay import SquadDisplay


class Mapa(metaclass=Singleton):
    def __init__(self, mapa):
        if hasattr(self, "_initialized"):
            return
        self._origin = (
            -Client().player.pos[0] + srodek[0],
            -Client().player.pos[1] + srodek[1],
        )
        self.origin1 = None
        self.width = 30
        self.height = 30
        self.mapa = AssetManager.maps[mapa]
        self.mapSurf = pygame.Surface((Mapa_width, Mapa_height))
        self.mapRect = self.mapSurf.get_frect(topleft=self.origin)
        self.tmx = load_pygame(join("Grafika/mapa", plik_mapy))
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

        self.split = None

        self.najechanie = Najechanie(
            AssetManager.get_asset("white_podswietlenie"),
            (tile_width / 2, tile_height / 2),
            AssetManager.get_asset(f"{Client().player.color}_podswietlenie"),
            AssetManager.get_asset(f"{Client().opponent.color}_podswietlenie"),
        )
        self.klikniecie = Klikniecie(
            AssetManager.get_asset("hex-klikniecie (2)"),
            (tile_width / 2, tile_height / 2),
        )
        self.import_state(Client().state)

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
        if original_origin[0] + offset[0] + Mapa_width < Width - mapa_x_offset:
            return False
        if original_origin[1] + offset[1] > mapa_y_offset:
            return False
        if original_origin[1] + offset[1] + Mapa_height < Height - mapa_y_offset:
            return False
        return True

    def load_tiles(self):
        x = 0
        y = 0
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
                )

                self.Tile_array[x][y] = tile
                x += 1
                x %= self.width
            y += 1

    def BFS(self, x1, y1, x2, y2):
        tablica_odwiedzonych = [
            [0 for _ in range(map_tile_width)] for _ in range(map_tile_height)
        ]
        tablica_odwiedzonych[x1][y1] = 1
        queue = Queue()
        queue.append((x1, y1))
        while not queue.empty():
            x, y = queue.pop()
            sasiedzix, sasiedziy = get_sasiedzi(x, y)
            for i in range(6):
                if x + sasiedzix[i] >= map_tile_width or x + sasiedzix[i] < 0:
                    continue
                if y + sasiedziy[i] >= map_tile_height or y + sasiedziy[i] < 0:
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
            [-1 for _ in range(map_tile_width)] for _ in range(map_tile_height)
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
        for budynek in self.building_group:
            budynek.draw(self.mapSurf)
        self.podswietlenie_group.draw(self.mapSurf)
        self.najechanie.draw(self.mapSurf)
        if flag.klikniecie_flag:
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

    def event(
        self,
        mouse_pos,
        flag,
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
                    flag.klikniecie_flag = True
                    self.klikniecie.origin = tile.pos

                    if self.move_flag is None:
                        self.move_flag = tile.jednostka
                        if (
                            not self.move_flag is None
                            and tile.jednostka.owner_id == Client().player.id
                            and Client().turn % 2 == Client().player.id
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
                                elif tile.jednostka.owner_id == Client().opponent.id:
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
                            if not tile.jednostka is None:
                                if (
                                    tile.jednostka.owner_id == Client().opponent.id
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
                        flag.klikniecie_flag = False
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
                self.move_flag.owner, self.move_flag.owner_id, self.move_flag.color
            )
            self.calculate_income()

    def recruit(self, tile):
        if (
            Client().player.gold
            > Client().player.frakcja["jednostka"][self.move_flag.wojownicy[3].id][
                "cost"
            ]
        ):
            Client().player.gold -= Client().player.frakcja["jednostka"][
                self.move_flag.wojownicy[3].id
            ]["cost"]
            self.move_flag.pos = tile.pos
            self.move_flag.tile = tile
            self.move_flag.ruch = self.correct_moves[tile.x][tile.y]
            tile.jednostka = self.move_flag
        else:
            print("not enough money")

    def recruit_join(self, tile):
        if (
            Client().player.gold
            > Client().player.frakcja["jednostka"][self.move_flag.wojownicy[3].id][
                "cost"
            ]
            and len(tile.jednostka) + len(self.move_flag) <= 7
        ):
            Client().player.gold -= Client().player.frakcja["jednostka"][
                self.move_flag.wojownicy[3].id
            ]["cost"]
            self.join(tile.jednostka, self.move_flag, tile)
        else:
            print("not enough money")

    def join(self, squad1, squad2, tile):
        squad2.ruch = self.correct_moves[tile.x][tile.y]

        squad1 = squad1 + squad2

        if not squad2.tile is None:
            squad2.tile.jednostka = None
        squad2.kill()

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

        for jednostka in state["jednostki"]:
            tile = self.get_tile(jednostka["pos"])
            if jednostka["owner_id"] == Client().player.id:
                frakcja = Client().player.frakcja
            else:
                frakcja = Client().opponent.frakcja
            s = Squad(self.army_group, jednostka, tile, frakcja)
            if Client().turn % 2 == s.owner_id and s.medyk:
                s.heal(frakcja["jednostka"][2]["heal"])  # medyk
            tile.jednostka = s

        for budynek in state["budynki"]:
            tile = self.get_tile(budynek["pos"])
            if budynek["owner_id"] == Client().player.id:
                frakcja = Client().player.frakcja
            else:
                frakcja = Client().opponent.frakcja
            if budynek["id"] == 0:
                b = Miasto(
                    self.building_group,
                    budynek,
                    tile,
                    frakcja,
                )
                if b.owner_id == Client().player.id:
                    tile.obrona = AssetManager.get_mnoznik(
                        "mury_upgrade", Client().player.akcje["mury_upgrade"]
                    )
                else:
                    tile.obrona = AssetManager.get_mnoznik(
                        "mury_upgrade", Client().opponent.akcje["mury_upgrade"]
                    )
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
            if budynek.owner_id == Client().player.id:
                budynek.tile.obrona = AssetManager.get_mnoznik(
                    "mury_upgrade", Client().player.akcje["mury_upgrade"]
                )
            else:
                budynek.tile.obrona = AssetManager.get_mnoznik(
                    "mury_upgrade", Client().opponent.akcje["mury_upgrade"]
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
