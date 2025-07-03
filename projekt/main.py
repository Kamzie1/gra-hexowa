from projekt.ustawienia import FPS
from projekt.network import Client
from projekt.kolejka import Kolejka
from projekt.pokoje import Pokoje
from projekt.gra import Gra
from projekt.spectator import Spectator
from sys import exit
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.client = Client()
        self.client.test()
        self.kolejka = Kolejka()
        self.gra_created = False
        self.spec_created = False
        self.pokoje_created = False

    def run(self):
        while True:
            match (self.client.ekran):
                case 0:
                    if not self.pokoje_created:
                        self.pokoje_created = True
                        self.pokoje = Pokoje()
                    self.pokoje.run(self.screen, self.client)
                case 1:
                    self.kolejka.run(self.screen, self.client)
                case 2:
                    if not self.gra_created:
                        print(self.client.name)
                        gra = Gra(self.client)
                        self.gra_created = True
                        self.pokoje_created = False
                        print("created game")
                    gra.run(self.screen)
                case 3:
                    if not self.spec_created:
                        print(self.client.name)
                        spec = Spectator(self.client)
                        self.spec_created = True
                        self.pokoje_created = False
                        print("created spec")
                    spec.run(self.screen)

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


if __name__ == "__main__":
    main = Main()
    main.run()
