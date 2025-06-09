import pygame
from os.path import join


class Display:
    def __init__(self, width, height, pos, font, font_size):
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_frect(topleft=pos)
        self.font = pygame.font.Font(join("grafika", font), font_size)

    def display(self, content, color):
        self.surf.fill((0, 0, 0))
        text = self.font.render(content, True, color)
        text_rect = text.get_frect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
