from ..ustawienia import *
from os.path import join
import pygame
from .button import Quit


class Resource:
    def __init__(self):
        self.surf = pygame.Surface((resource_width, resource_height), pygame.SRCALPHA)
        self.surf.fill(resource_color)
        self.rect = self.surf.get_frect(topleft=resource_pos)
        self.font = pygame.font.Font(join(folder_grafiki, font), font_size)
        self.button_group = pygame.sprite.Group()
        Quit(
            50,
            50,
            "blue",
            (0, 0),
            self.button_group,
        )

    def fill(self):
        self.surf.fill(resource_color)

    def display_gold(self, player, pos):
        image = pygame.image.load(join("grafika", "złoto.png"))
        rect = image.get_frect(topleft=(150, (resource_height - font_size) / 2))
        self.surf.blit(image, rect)
        display = f"{player.gold} "
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=pos)
        self.surf.blit(text, text_rect)
