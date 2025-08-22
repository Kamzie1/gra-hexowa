import pygame
from projekt.narzedzia import pozycja_myszy_na_surface, clicked
from os.path import join
from projekt.ustawienia import folder_grafiki, tile_height, tile_width
from projekt.assetMenager import AssetManager


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        pos,
        group,
        id,
        koszt_ruchu,
        typ,
        image,
        obrona,
        widocznosc,
        budynek=None,
        jednostka=None,
    ) -> None:
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_frect(center=pos)
        self.id = id
        self.budynek = budynek
        self.jednostka = jednostka
        self.pos = pos
        self.koszt_ruchu = koszt_ruchu
        self.typ = typ
        self.obrona = obrona
        self.widocznosc = widocznosc

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Najechanie:
    def __init__(self, pos):
        self._origin = pos
        self.rect = AssetManager.get_asset("white_podswietlenie").get_frect(
            center=self.origin
        )
        self.display = "0"
        self.flag = "white"

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = AssetManager.get_asset(f"{self.flag}_podswietlenie").get_frect(
            center=self.origin
        )

    def update(self, mouse_pos, Tile_array, origin):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, origin)

        for tiles in Tile_array:
            for tile in tiles:
                if clicked(tile.pos, mouse_pos):
                    self.origin = tile.pos
                    # dodac widok zachowanie dla nie widocznej czesic
                    if tile.jednostka is not None:
                        self.flag = tile.jednostka.color
                    elif tile.budynek is not None:
                        self.flag = tile.budynek.color
                    else:
                        self.flag = "white"
                    self.display = str(int(tile.obrona * 100)) + "%"

    def draw(self, screen):
        surf = AssetManager.get_asset(f"{self.flag}_podswietlenie")
        font = AssetManager.get_font("consolas", 24)
        text = font.render(self.display, True, "black")
        text_rect = text.get_rect(center=self.origin)
        screen.blit(text, text_rect)
        screen.blit(surf, self.rect)


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
        self.image = surf.copy()
        self.rect = self.image.get_frect(center=self.origin)
        font = AssetManager.get_font("consolas", 16)
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
