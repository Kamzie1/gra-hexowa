from ..ustawienia import *
from ..jednostki import *
from os.path import join
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(button_group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_frect(topleft=self.pos)
        self.font = pygame.font.Font(join(folder_grafiki, font), font_size)
        self.text = "button"

    def display(self):
        self.display = self.font.render(self.text, True, "black")
        self.text_rect = self.display.get_rect(topleft=self.pos)
        self.image.blit(self.display, self.text_rect)


class Recruit(Button):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        jednostka,
        group,
        button_group,
        recruit_pos,
        player,
        mapa,
    ) -> None:
        super().__init__(width, height, color, pos, button_group)
        self.group = group
        self.text = f"{jednostka['nazwa']}"
        self.recruit_pos = recruit_pos
        self.jednostka = jednostka
        self.player = player
        self.mapa = mapa
        print("button gotowy")

    def click(self):
        try:
            if self.mapa.Tile_array[pos_rec_x][pos_rec_y].jednostka is None:
                self.player.gold -= self.jednostka["cost"]
                w = Wojownik(
                    self.jednostka,
                    self.group,
                    self.recruit_pos,
                    self.mapa.Tile_array[pos_rec_x][pos_rec_y],
                )
                self.mapa.Tile_array[pos_rec_x][pos_rec_y].jednostka = w
        except (ValueError, TypeError) as e:
            print(e)


class Quit(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group)
        self.text = "quit"

    def click(self, show):
        return not show
