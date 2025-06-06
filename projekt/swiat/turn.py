import pygame
from ..ustawienia import Width, Height


class Turn:
    def __init__(self):
        self.image = pygame.Surface((80, 80))
        self.image.fill("blue")
        self.rect = self.image.get_frect(bottomright=(Width, Height))

    def event(self, mouse_pos, army_group):
        if self.rect.collidepoint(mouse_pos):
            print("koniec")
            for jednostka in army_group:
                jednostka.ruch = jednostka.original_ruch

    def draw(self, screen):
        screen.blit(self.image, self.rect)
