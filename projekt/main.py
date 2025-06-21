from projekt.ustawienia import FPS
from projekt.network import Client
from projekt.kolejka import Kolejka
from projekt.pokoje import Pokoje
from sys import exit
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))  # okienko
        pygame.display.set_caption("Main")
        self.screen.fill("white")
        self.clock = pygame.time.Clock()
        self.client = Client()
        self.client.test()
        self.pokoje = Pokoje()
        self.kolejka = Kolejka()

    def run(self):
        while True:
            self.screen.fill("white")
            self.event_handler()
            match (self.client.ekran):
                case 0:
                    self.pokoje.draw(self.screen)
                case 1:
                    self.kolejka.draw()

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS

    def event_handler(self):
        self.pokoje.game_event(self.client)
        self.pokoje.error_event(self.client)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.pokoje.name_input.update(event)
            self.pokoje.id_input.update(event)
            self.pokoje.join_event(event, self.client)
            self.pokoje.create_event(event, self.client)


if __name__ == "__main__":
    main = Main()
    main.run()
