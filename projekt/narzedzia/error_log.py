import pygame
from projekt.assetMenager import AssetManager


class Error_log:
    def __init__(self, w, h, pos, color):
        self.surf = pygame.Surface((w, h))
        self.surf.fill(color)
        self.color = color
        self.rect = self.surf.get_frect(topleft=pos)
        self.font = AssetManager.get_font("consolas", 24)
        self.error = ""
        self.font_color = "red"

    def display_error(self, error, color):
        self.error = error
        self.font_color = color

    def draw(self, screen):
        self.surf.fill(self.color)
        text = self.font.render(self.error, True, self.font_color)
        text_rect = text.get_rect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
