import pygame
from ..ustawienia import Width, Height


class Turn:
    def __init__(self):
        self.image = pygame.image.load("Grafika/turn.png").convert_alpha()
        self.rect = self.image.get_frect(bottomright = (Width-15, Height-15))

    def event(self, mouse_pos, mapa, client):
        if self.rect.collidepoint(mouse_pos) and client.turn % 2 == client.id:
            new_state = mapa.load_state()
            client.send_state(new_state)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

