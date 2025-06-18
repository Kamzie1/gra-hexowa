import pygame
from projekt.ustawienia import folder_grafiki, font
from os.path import join


class Przycisk:
    def __init__(self, width, height, color, pos, tekst, font_color) -> None:
        self.surf = pygame.Surface((width, height))
        self.color = color
        self.surf.fill(color)
        self.pos = pos
        self.rect = self.surf.get_frect(topleft=self.pos)
        self.display = tekst
        self.font = pygame.font.Font(join(folder_grafiki, font), 24)
        self.font_color = font_color

    def draw(self, screen):
        self.surf.fill(self.color)
        text = self.font.render(self.display, True, self.font_color)
        text_rect = text.get_rect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
