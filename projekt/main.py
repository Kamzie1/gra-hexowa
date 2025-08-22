from projekt.ustawienia import FPS
from projekt.network import Client
from projekt.kolejka import Kolejka
from projekt.pokoje import Pokoje
from projekt.gra import Gra
from projekt.spectator import Spectator
from sys import exit
import pygame
from projekt.assetMenager import AssetManager


class Main:
    def __init__(self):
        pygame.init()
        Client()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("gra hexowa")
        self.clock = pygame.time.Clock()
        AssetManager.preload_assets()
        Client().test()
        self.kolejka = Kolejka()
        self.gra_created = False
        self.spec_created = False
        self.pokoje_created = False

    def run(self):
        while True:
            match (Client().ekran):
                case 0:
                    if not self.pokoje_created:
                        self.pokoje_created = True
                        self.pokoje = Pokoje()
                    self.pokoje.run(self.screen)
                case 1:
                    self.kolejka.run(self.screen)
                case 2:
                    if not self.gra_created:
                        gra = Gra()
                        self.gra_created = True
                        self.pokoje_created = False
                        print("created game")
                    gra.run(self.screen)
                case 3:
                    if not self.spec_created:
                        spec = Spectator()
                        self.spec_created = True
                        self.pokoje_created = False
                        print("created spec")
                    spec.run(self.screen)

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


if __name__ == "__main__":
    main = Main()
    main.run()
