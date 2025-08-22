import pygame
from projekt.ustawienia import Width, Height
from projekt.assetMenager import AssetManager
from projekt.narzedzia import Singleton
from projekt.network import Client
from .mapa import Mapa


class Turn(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.image = AssetManager.get_asset("turn")
        self.surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 100))
        self.rect = self.image.get_frect(topleft=(0, 0))
        self.drect = self.surf.get_frect(bottomright=(Width - 15, Height - 15))

    def event(self, mouse_pos):
        if (
            self.drect.collidepoint(mouse_pos)
            and Client().turn % len(Client().users) == Client().id
        ):
            new_state = Mapa().load_state()
            Client().send_state(new_state)

    def draw(self, screen):
        self.surf.blit(self.image, self.rect)
        screen.blit(self.surf, self.drect)
