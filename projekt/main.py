from projekt.jednostki import Japonia
from projekt.narzedzia import oblicz_pos, Input, Przycisk, Error_log
from projekt.ustawienia import FPS
from projekt.network import Client
from projekt.gra import Gra
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))  # okienko
        pygame.display.set_caption("Main")
        self.screen.fill("white")
        self.clock = pygame.time.Clock()
        self.name_input = Input(
            300, 34, (100, 100), "grey", "black", "podaj swoje imię:"
        )
        self.id_input = Input(300, 34, (100, 150), "grey", "black", "wpisz id pokoju:")
        self.join = Przycisk(70, 34, "blue", (450, 150), "Join", "grey")
        self.create = Przycisk(200, 34, "green", (100, 200), "stwórz pokój", "black")
        self.error_log = Error_log(300, 34, (100, 0), "antiquewhite3")
        self.client = Client()
        self.client.start()

    def run(self):
        while True:
            self.event_handler()
            self.draw()

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS

    def event_handler(self):
        self.game_event()
        self.error_event()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wyjdź z programu
                pygame.quit()
                self.client.stop()
                exit()

            self.name_input.update(event)
            self.id_input.update(event)
            self.join_event(event)
            self.create_event(event)

    def draw(self):
        self.name_input.draw(self.screen)
        self.id_input.draw(self.screen)
        self.join.draw(self.screen)
        self.create.draw(self.screen)
        self.error_log.draw(self.screen)

    def join_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.join.rect.collidepoint(pygame.mouse.get_pos()):
                if (
                    len(self.name_input.display) == 0
                    or len(self.id_input.display) == 0
                    or self.name_input.display == self.name_input.message
                    or self.id_input.display == self.id_input.message
                ):
                    return
                self.client.join_room(self.id_input.display, self.name_input.display)

    def create_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.create.rect.collidepoint(pygame.mouse.get_pos()):
                if (
                    len(self.name_input.display) == 0
                    or self.name_input.display == self.name_input.message
                ):
                    return
                self.client.create_room(self.name_input.display)

    def game_event(self):
        if self.client.start_game:
            self.client.start_game = False
            pygame.quit
            gra = Gra(self.client)
            gra.run()

    def error_event(self):
        if self.client.connected:
            self.error_log.display_error("connected", "green")
        else:
            self.error_log.display_error("not connected", "red")


if __name__ == "__main__":
    main = Main()
    main.run()
