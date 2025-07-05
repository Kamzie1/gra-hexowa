import pygame
from sys import exit
from projekt.ustawienia import *  # plik z ustawieniami
from projekt.swiat import (
    Mapa,
    Mini_map,
    Resource,
    SideMenu,
    Turn,
    SquadButtonDisplay,
    Exit,
)
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


class Spectator:
    def __init__(self, client):
        for user in client.spectators:
            if user["name"] == client.name:
                self.player = Player(user)
        # obiekty
        self.clock = pygame.time.Clock()
        self.attackDisplay = AttackDisplay(Width / 1.2, Height / 1.2, srodek, "black")
        self.mapa = Mapa(
            srodek,
            self.player,
            client.users,
            client.state,
            1,
            client.map,
            client.width,
            client.height,
        )
        self.mini_mapa = Mini_map(srodek, self.mapa.Mapa_width, self.mapa.Mapa_height)
        self.button_group = pygame.sprite.Group()
        self.exit = Exit(50, 50, "red", (5, 5), self.button_group)
        self.flag = Flag()
        self.client = client
        self.client.mapa = self.mapa
        self.client.id = -1
        self.turn_display = TurnDisplay(
            300, 34, (srodek[0] - 25, 0), "consolas.ttf", 20
        )
        self.squadDisplay = SquadDisplay(Width / 2, Height / 2, srodek, "black")
        self.DisplaySquadButton = SquadButtonDisplay(
            80, 80, "blue", (srodek[0], Height - 50)
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
        self.button_group.draw(screen)
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

        if self.squadDisplay.show and not self.mapa.move_flag is None:
            self.squadDisplay.display(self.mapa.move_flag, screen)

        if self.client.koniecGry.show:
            self.client.koniecGry.draw(screen)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.client.koniecGry.show:
                    self.client.ekran = 0

                self.mapa.event(
                    mouse_pos,
                    self.flag,
                    self.client.turn,
                    self.squadDisplay,
                    self.DisplaySquadButton,
                    self.attackDisplay,
                    self.client.id,
                )
                self.DisplaySquadButton.event(
                    mouse_pos, self.squadDisplay, self.mapa.move_flag
                )
                for button in self.button_group:
                    if button.rect.collidepoint(mouse_pos):
                        button.click(self.client)
