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
    Rotate,
    SquadDisplay,
)
from projekt.player import Player
from projekt.narzedzia import (
    oblicz_pos,
    TurnDisplay,
    KoniecGry,
    AttackDisplay,
    Display,
    MouseDisplay,
)
from projekt.flag import Flag
from projekt.network import Client
from .assetMenager import AssetManager
from .animationMenager import AnimationMenager


class Spectator:
    def __init__(self):

        # obiekty
        Mapa(1)
        Client().mapa = Mapa(0)
        Mini_map()
        Resource()
        Flag()
        KoniecGry(Width, Height)
        self.turn_Display = TurnDisplay(300, 34, (srodek[0] - 25, 0), "consolas", 20)
        SquadDisplay(Width / 2, Height / 2, srodek, "black")
        self.squadButtonDisplay = SquadButtonDisplay(
            80, 80, "blue", (srodek[0] - 50, Height - 50)
        )
        self.rotateButton = Rotate(80, 80, "red", (srodek[0] + 50, Height - 50))
        AttackDisplay(Width / 1.2, Height / 1.2, srodek, "black")

    # metoda uruchamiająca grę
    def run(self, screen):
        if not Client().state_loaded:
            return

        self.update()  # mouse hover

        self.event_handler()  # event (kliknięcie)

        self.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        MouseDisplay().show = False
        Resource().update()
        self.turn_Display.hover(mouse_pos, Client().pogoda[0])
        if SquadDisplay().show:
            SquadDisplay().update(pygame.mouse.get_pos())

        if Mapa().move_flag is not None:
            if self.squadButtonDisplay.rect.collidepoint(mouse_pos):
                MouseDisplay().update(mouse_pos, "Statystyki oddziału")

        Mapa().update()
        Mini_map().update()
        AnimationMenager.update()

    def draw(self, screen):
        screen.fill("black")
        Mapa().draw(screen)
        Resource().draw(screen)
        self.turn_Display.display(
            "grey", screen, Client().users, Client().turn, Client().pogoda[0]
        )
        Mini_map().draw(screen)
        for jednostka in Mapa().army_group:
            jednostka.draw(Mapa().mapSurf)

        if not Mapa().move_flag is None:
            screen.blit(self.squadButtonDisplay.image, self.squadButtonDisplay.rect)

        if SquadDisplay().show and not Mapa().move_flag is None:
            SquadDisplay().display(Mapa().move_flag, screen)
        if KoniecGry().show:
            KoniecGry().draw(screen)
        MouseDisplay().draw(screen)

    def event_handler(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if KoniecGry().show:
                    pygame.quit()
                    exit()

                Mapa().event(
                    mouse_pos,
                    self.squadButtonDisplay,
                    self.rotateButton,
                )

                Resource().event(mouse_pos)
                self.squadButtonDisplay.event(mouse_pos, Mapa().move_flag)

                if SquadDisplay().show:
                    SquadDisplay().event(
                        mouse_pos, Mapa().move_flag, Client().player.id, Mapa()
                    )
