import pygame
from ..ustawienia import Width, Height


class Turn:
    def __init__(self):
        self.image = pygame.Surface((80, 80))
        self.image.fill("blue")
        self.rect = self.image.get_frect(bottomright=(Width, Height))
