from projekt.narzedzia import Input, Przycisk, Error_log
import pygame
from sys import exit
from projekt.ustawienia import Width, Height, srodek
from projekt.network import Client


class Pokoje:
    def __init__(self):
        self.exit = Przycisk(100, 34, "red", (0, 0), "Wyjdź", "white")
        self.name_input = Input(
            300, 34, (100, 100), "grey", "black", "podaj swoje imię:"
        )
        self.id_input = Input(300, 34, (100, 150), "grey", "black", "wpisz id pokoju:")
        self.join = Przycisk(70, 34, "blue", (450, 150), "Join", "grey")
        self.create = Przycisk(200, 34, "green", (100, 200), "stwórz pokój", "black")
        self.error_log = Error_log(300, 34, (srodek[0], 0), "antiquewhite3")

    def run(self, screen):
        self.event_handler()
        self.draw(screen)

    def draw(self, screen):
        screen.fill("white")
        self.name_input.draw(screen)
        self.id_input.draw(screen)
        self.join.draw(screen)
        self.create.draw(screen)
        self.error_log.draw(screen)
        self.exit.draw(screen)

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
                Client().join_room(self.id_input.display, self.name_input.display)

    def create_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.create.rect.collidepoint(pygame.mouse.get_pos()):
                if (
                    len(self.name_input.display) == 0
                    or self.name_input.display == self.name_input.message
                ):
                    return

                Client().create_room(self.name_input.display)

    def exit_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.exit.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                exit()

    def error_event(self):
        if Client().connected:
            self.error_log.display_error("connected", "green")
        else:
            self.error_log.display_error("not connected", "red")

    def event_handler(self):
        self.error_event()
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.exit_event(event)
            self.name_input.update(event, mouse_pos)
            self.id_input.update(event, mouse_pos)
            self.join_event(event)
            self.create_event(event)
