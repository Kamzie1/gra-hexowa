import pygame
from sys import exit
from projekt.ustawienia import *  # plik z ustawieniami
from projekt.swiat import Mapa, Mini_map, Resource, SideMenu, Turn, SquadButtonDisplay
from projekt.player import Player
from projekt.narzedzia import (
    oblicz_pos,
    TurnDisplay,
    SquadDisplay,
    KoniecGry,
    AttackDisplay,
    Display,
)
from projekt.flag import Flag
from projekt.jednostki import get_fraction
from projekt.network import Client


class Gra:
    def __init__(self, client):
        for user in client.users:
            if user["name"] == client.name:
                self.player = Player(user)
        # obiekty
        self.clock = pygame.time.Clock()
        self.mini_mapa = Mini_map(self.player.recruit_pos)
        self.attackDisplay = AttackDisplay(Width / 1.2, Height / 1.2, srodek, "black")
        self.mapa = Mapa(
            self.player.recruit_pos, self.player, client.users, client.state
        )
        self.resource = Resource()
        self.turn = Turn()
        self.menu = SideMenu(self.player, self.mapa)
        self.flag = Flag()
        self.client = client
        self.client.mapa = self.mapa
        self.turn_display = TurnDisplay(
            300, 34, (srodek[0] - 25, 0), "consolas.ttf", 20
        )
        self.squadDisplay = SquadDisplay(Width / 2, Height / 2, srodek, "black")
        self.DisplaySquadButton = SquadButtonDisplay(
            80, 80, "blue", (srodek[0], Height - 50)
        )
        self.not_you_turnDisplay = Display(
            Width / 2, 100, (srodek[0] - Width / 4, srodek[1] / 2), "consolas.ttf", 100
        )

    # metoda uruchamiająca grę
    def run(self, screen):
        if not self.client.state_loaded:
            self.clock.tick(FPS)
            return
        self.event_handler()

        self.update()
        self.draw(screen)  # rysuje wszystkie elementy

    def update(self):
        self.mapa.update()
        self.mini_mapa.update(self.mapa)

    def draw(self, screen):
        screen.fill("black")
        self.mapa.draw(screen, self.flag)
        if self.flag.show:
            self.menu.draw(screen)
        self.resource.draw(screen, self.player)
        self.turn_display.display("grey", screen, self.client.turn, self.client.users)
        self.mini_mapa.draw(
            screen,
            self.mapa.origin,
            self.mapa.Tile_array,
            self.mapa.widok,
            self.mapa.widziane,
        )

        if not self.mapa.move_flag is None:
            screen.blit(self.DisplaySquadButton.image, self.DisplaySquadButton.rect)
        if self.attackDisplay.show:
            self.attackDisplay.display(screen)

        self.turn.draw(screen)
        if self.client.turn % len(self.client.users) != self.player.id:
            self.not_you_turnDisplay.display(
                "Tura Przeciwnika", self.player.color, screen
            )

        if self.squadDisplay.show and not self.mapa.move_flag is None:
            self.squadDisplay.display(self.mapa.move_flag, screen)
        if self.client.koniecGry.show:
            self.client.koniecGry.draw(screen)

    def event_handler(self):
        if self.mapa.Tile_array[self.player.x][self.player.y].jednostka is None:
            self.client.send_result(self.client.name)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.client.koniecGry.show:
                    self.client.ekra = 0

                self.mapa.event(
                    mouse_pos,
                    self.flag,
                    self.client.turn,
                    self.squadDisplay,
                    self.DisplaySquadButton,
                    self.attackDisplay,
                )

                self.turn.event(mouse_pos, self.mapa, self.client)
                self.resource.event(mouse_pos, self.flag, self.client)
                self.menu.event(
                    mouse_pos,
                    self.flag,
                    self.client.turn,
                    self.client.id,
                    self.client.users,
                )
                self.DisplaySquadButton.event(
                    mouse_pos, self.squadDisplay, self.mapa.move_flag
                )
