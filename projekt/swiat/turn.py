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
            and Client().turn % 2 == Client().player.id
        ):
            new_state = Mapa().load_state()
            Mapa().import_state(new_state)
            Client().send_state(new_state)
            if Client().turn % 2 == Client().player.id and Client().turn != 1:
                Mapa().zarabiaj()
                Mapa().heal()

    def draw(self, screen):
        self.surf.blit(self.image, self.rect)
        screen.blit(self.surf, self.drect)
