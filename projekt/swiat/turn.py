import pygame
from ..ustawienia import Width, Height


class Turn:
    def __init__(self):
        self.image = pygame.image.load("Grafika/turn.png").convert_alpha()
        self.surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 100))
        self.rect = self.image.get_frect(topleft=(0, 0))
        self.drect = self.surf.get_frect(bottomright=(Width - 15, Height - 15))

    def event(self, mouse_pos, mapa, client):
        if (
            self.drect.collidepoint(mouse_pos)
            and client.turn % len(client.users) == client.id
        ):
            new_state = mapa.load_state()
            client.send_state(new_state)

    def draw(self, screen):
        self.surf.blit(self.image, self.rect)
        screen.blit(self.surf, self.drect)
