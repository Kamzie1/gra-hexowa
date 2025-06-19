import pygame
from projekt.ustawienia import srodek


class KoniecGry:
    def __init__(self, width, height):
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 100))
        self.rect = self.surf.get_rect(topleft=(0, 0))
        self.show = False
        self.result = ""
        self.font = pygame.font.Font("Grafika/mapa/consolas.ttf", 100)

    def display(self, result, color):
        self.show = True
        self.result = result
        self.color = color

    def draw(self, screen):
        text = self.font.render(self.result, True, self.color)
        text_rect = text.get_rect(center=srodek)
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
