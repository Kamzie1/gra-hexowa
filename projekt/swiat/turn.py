import pygame
from projekt.ustawienia import Width, Height
from projekt.assetMenager import AssetManager
from projekt.narzedzia import Singleton
from projekt.network import Client
from .mapa import Mapa
from .sidemenu import SideMenu
from projekt.bot import Bot


class Turn(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.image = AssetManager.get_asset("turn")
        self.surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 100))
        self.rect = self.image.get_frect(topleft=(0, 0))
        self.drect = self.surf.get_frect(bottomright=(Width - 15, Height - 15))

    def event(self, mouse_pos, bot):
        if (
            self.drect.collidepoint(mouse_pos)
            and Client().turn % 2 == Client().player.id
        ):
            new_state = Mapa().load_state()
            if Client().turn % 2 == Client().player.id and Client().turn != 1:
                Client().player.earn()
            Client().send_state(new_state)
            new_state = bot.turn(
                new_state,
                {"mapa": Mapa().mapa, "width": Mapa().width, "height": Mapa().height},
                Client().info[Client().opponent.name],
            )
            Client().turn += 1
            Mapa().import_state(new_state)
            Client().player.akcjeMenager.turn()
            if Client().turn % 2 == Client().player.id and Client().turn != 1:
                Mapa().heal()
            Mapa().swap()
            SideMenu().swap(Client().player)

    def draw(self, screen):
        self.surf.blit(self.image, self.rect)
        screen.blit(self.surf, self.drect)
