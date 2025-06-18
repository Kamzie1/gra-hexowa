from projekt.narzedzia import Input, Przycisk, Error_log
import pygame
from projekt.gra import Gra


class Pokoje:
    def __init__(self):
        self.name_input = Input(
            300, 34, (100, 100), "grey", "black", "podaj swoje imię:"
        )
        self.id_input = Input(300, 34, (100, 150), "grey", "black", "wpisz id pokoju:")
        self.join = Przycisk(70, 34, "blue", (450, 150), "Join", "grey")
        self.create = Przycisk(200, 34, "green", (100, 200), "stwórz pokój", "black")
        self.error_log = Error_log(300, 34, (100, 0), "antiquewhite3")

    def draw(self, screen):
        pygame.display.set_caption("Pokoje")
        self.name_input.draw(screen)
        self.id_input.draw(screen)
        self.join.draw(screen)
        self.create.draw(screen)
        self.error_log.draw(screen)

    def join_event(self, event, client):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.join.rect.collidepoint(pygame.mouse.get_pos()):
                if (
                    len(self.name_input.display) == 0
                    or len(self.id_input.display) == 0
                    or self.name_input.display == self.name_input.message
                    or self.id_input.display == self.id_input.message
                ):
                    return
                client.join_room(self.id_input.display, self.name_input.display)

    def create_event(self, event, client):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.create.rect.collidepoint(pygame.mouse.get_pos()):
                if (
                    len(self.name_input.display) == 0
                    or self.name_input.display == self.name_input.message
                ):
                    return
                client.create_room(self.name_input.display)

    def game_event(self, client):
        if client.start_game:
            client.start_game = False
            pygame.quit
            gra = Gra(client)
            gra.run()

    def error_event(self, client):
        if client.connected:
            self.error_log.display_error("connected", "green")
        else:
            self.error_log.display_error("not connected", "red")
