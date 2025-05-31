from ustawienia import *
from os.path import join
import pygame


class Resource:
    def __init__(self):
        self.surf = pygame.Surface((resource_width, resource_height))
        self.surf.fill(resource_color)
        self.rect = self.surf.get_frect(topleft=resource_pos)
        self.font = pygame.font.Font(join(folder_grafiki, font), font_size)

    def fill(self):
        self.surf.fill(resource_color)

    def display_gold(self, player, pos):
        self.display = f"Gold: {player.gold} "
        self.text = self.font.render(self.display, True, font_color)
        self.text_rect = self.text.get_rect(topleft=pos)
        self.surf.blit(self.text, self.text_rect)
