from ustawienia import *
from jednostki import *
from os.path import join
import pygame


class SideMenu:
    def __init__(self, player, group):
        self.surf = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        self.surf.fill(menu_color)
        self.rect = self.surf.get_frect(topleft=menu_pos)
        self.player = player
        self.group = group
        self.button_group = pygame.sprite.Group()

        Recruit(
            50,
            50,
            "red",
            (0, 0),
            Yukimura_Sanada,
            self.group,
            self.button_group,
            recruit_pos,
            self.player,
        )

    def fill(self):
        self.surf.fill(menu_color)


class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, color, pos, group, button_group) -> None:
        super().__init__(button_group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_frect(topleft=self.pos)
        self.font = pygame.font.Font(join(folder_grafiki, font), font_size)
        self.text = "button"

        self.group = group

    def click(self):
        pass

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
    ) -> None:
        super().__init__(width, height, color, pos, group, button_group)
        self.text = f"{jednostka['nazwa']}"
        self.recruit_pos = recruit_pos
        self.jednostka = jednostka
        self.player = player
        print("button gotowy")

    def click(self):
        try:
            self.player.gold -= self.jednostka["cost"]
            Wojownik(self.jednostka, self.group, self.recruit_pos)
        except (ValueError, TypeError) as e:
            print(e)
