from projekt.ustawienia import FPS
from projekt.network import Client
from projekt.kolejka import Kolejka
from projekt.pokoje import Pokoje
from projekt.gra import Gra
from sys import exit
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.client = Client()
        self.client.start()
        self.pokoje = Pokoje()
        self.kolejka = Kolejka()
        self.gra_created = False

    def run(self):
        while True:
            match (self.client.ekran):
                case 0:
                    self.pokoje.run(self.screen, self.client)
                case 1:
                    self.kolejka.run(self.screen, self.client)
                case 2:
                    if not self.gra_created:
                        gra = Gra(self.client)
                        self.gra_created = True
                        print("created game")
                    gra.run(self.screen)

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


if __name__ == "__main__":
    main = Main()
    main.run()
