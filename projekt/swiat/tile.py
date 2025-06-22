import pygame
from ..narzedzia import pozycja_myszy_na_surface, clicked
from os.path import join
from ..ustawienia import folder_grafiki, tile_height, tile_width


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        surf,
        x,
        y,
        pos,
        group,
        id,
        koszt_ruchu,
        widocznosc,
        typ,
        budynek=None,
        jednostka=None,
    ) -> None:
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.id = id
        self.budynek = budynek
        self.jednostka = jednostka
        self.pos = pos
        self.koszt_ruchu = koszt_ruchu
        self.typ = typ
        self.widocznosc = widocznosc
        self.chmura_surf = pygame.image.load(
            "Grafika/tile-grafika/efekty hexów/chmura_weak2.png"
        ).convert_alpha()
        self.chmura_rect = self.chmura_surf.get_frect(center=self.pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def drawChmura(self, screen):
        screen.blit(self.chmura_surf, self.chmura_rect)


class Najechanie:
    def __init__(self, base, pos, red, blue):
        self._origin = pos
        self.surf = [base, red, blue]
        self.rect = self.surf[0].get_frect(center=self.origin)

        self.flag = -1

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = self.surf[0].get_frect(center=self.origin)

    def update(
        self, mouse_pos, Tile_array, origin, player_id, opponent_id, widok, widziane
    ):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, origin)

        for tiles in Tile_array:
            for tile in tiles:
                if clicked(tile.pos, mouse_pos):
                    self.origin = tile.pos
                    if widok[tile.x][tile.y] < 0:
                        if widziane[tile.x][tile.y]:
                            self.flag = 0
                        else:
                            self.flag = -1
                    elif tile.jednostka is None:
                        self.flag = 0
                    elif tile.jednostka.owner_id == player_id:
                        self.flag = 1
                    elif tile.jednostka.owner_id == opponent_id:
                        self.flag = 2


class Klikniecie:
    def __init__(self, image, pos):
        self._origin = pos
        self.image = image
        self.rect = self.image.get_frect(center=self.origin)

        self.flag = -1

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = self.image.get_frect(center=self.origin)


class Ruch(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos, ruch):
        super().__init__(groups)
        self._origin = pos
        self.image = surf
        self.rect = self.image.get_frect(center=self.origin)
        font = pygame.font.Font(join("Grafika/fonts", "consolas.ttf"), 16)
        display = f"{ruch}"
        text = font.render(display, True, "black")
        text_rect = text.get_rect(center=(tile_width / 2, tile_height / 2))
        self.image.blit(text, text_rect)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = self.image.get_frect(center=self.origin)


class Podswietlenie(pygame.sprite.Sprite):
    def __init__(self, url, pos, group):
        super().__init__(group)
        self.image = pygame.image.load(f"Grafika/tile-grafika/efekty hexów/{url}")
        self.rect = self.image.get_frect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Chmura(pygame.sprite.Sprite):
    def __init__(self, pos, group, type):
        super().__init__(group)
        match (type):
            case "weak":
                self.image = pygame.image.load(
                    "Grafika/tile-grafika/efekty hexów/chmura_weak.png"
                )
            case "strong":
                self.image = pygame.image.load(
                    "Grafika/tile-grafika/efekty hexów/chmura_strong.png"
                )
        self.rect = self.image.get_frect(center=pos)
