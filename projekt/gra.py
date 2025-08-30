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
    AttackDisplay,
    Wzmocnienie,
    InzynierBuild,
    InzynierButton,
)
from projekt.player import Player
from projekt.narzedzia import oblicz_pos, TurnDisplay, KoniecGry, MouseDisplay, Display
from projekt.flag import Flag
from projekt.network import Client
from .assetMenager import AssetManager
from .animationMenager import AnimationMenager
from projekt.jednostki import Squad


class Gra:
    def __init__(self):

        # obiekty
        Mapa(
            0,
            (
                -Client().player.pos[0] + srodek[0],
                -Client().player.pos[1] + srodek[1],
            ),
        )
        Client().mapa = Mapa(0)
        Mini_map()
        AttackDisplay(Width / 1.2, Height / 1.2, srodek, "black")
        self.inzynierBuild = InzynierBuild(Width / 2, Height / 2, srodek)
        Resource()
        Turn()
        SideMenu()
        Flag()
        KoniecGry(Width, Height)
        self.turn_Display = TurnDisplay(500, 34, (srodek[0] - 25, 0), "consolas", 20)
        SquadDisplay(Width / 2, Height / 2, srodek, "black")
        self.squadButtonDisplay = SquadButtonDisplay(
            80, 80, "blue", (srodek[0] - 50, Height - 50)
        )
        self.not_you_turnDisplay = Display(
            Width / 2, 100, (srodek[0] - Width / 4, srodek[1] / 2), "consolas", 100
        )
        self.rotateButton = Rotate(80, 80, "red", (srodek[0] + 50, Height - 50))
        self.wzmocnienieButton = Wzmocnienie(
            80, 80, "blue", (srodek[0] + 150, Height - 50)
        )
        self.inzynierButton = InzynierButton(
            80, 80, "red", (srodek[0] + 250, Height - 50)
        )

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
        SideMenu().update()
        Resource().update()
        self.turn_Display.hover(
            mouse_pos, Client().pogoda, Client().player.akcje["wheater_forecast"]
        )
        if SquadDisplay().show:
            SquadDisplay().update(pygame.mouse.get_pos())

        if Mapa().move_flag is not None and isinstance(Mapa().move_flag, Squad):
            if self.squadButtonDisplay.rect.collidepoint(mouse_pos):
                MouseDisplay().update(mouse_pos, "Statystyki oddziału")

            if self.rotateButton.rect.collidepoint(mouse_pos):
                MouseDisplay().update(mouse_pos, "Obróć oddział")

            if self.wzmocnienieButton.rect.collidepoint(mouse_pos):
                MouseDisplay().update(
                    mouse_pos, "Wzmocnij oddział (+5% obrony) za 4 ruchu"
                )
            if Mapa().move_flag.inzynier():
                self.inzynierButton.hover(mouse_pos)

        if AttackDisplay().show:
            AttackDisplay().hover(pygame.mouse.get_pos())

        Mapa().update()
        Mini_map().update()
        AnimationMenager.update()

    def draw(self, screen):
        screen.fill("black")
        Mapa().draw(screen)
        if Client().turn % len(Client().users) != Client().id:
            self.not_you_turnDisplay.display(
                "Tura Przeciwnika", Client().player.color, screen
            )
        if Flag().show:
            SideMenu().draw(screen)
        Resource().draw(screen)
        self.turn_Display.display(
            "grey",
            screen,
            Client().users,
            Client().turn,
            Client().pogoda,
            Client().player.akcje["wheater_forecast"],
        )
        Mini_map().draw(screen)
        for jednostka in Mapa().army_group:
            jednostka.draw(Mapa().mapSurf)

        if not Mapa().move_flag is None and isinstance(Mapa().move_flag, Squad):
            screen.blit(self.squadButtonDisplay.image, self.squadButtonDisplay.rect)
            if Client().player.id == Mapa().move_flag.owner_id:
                screen.blit(self.rotateButton.image, self.rotateButton.rect)
                screen.blit(self.wzmocnienieButton.image, self.wzmocnienieButton.rect)
                if Mapa().move_flag.inzynier():
                    self.inzynierButton.draw(screen)
        if AttackDisplay().show:
            AttackDisplay().display(screen)

        if self.inzynierBuild.show:
            self.inzynierBuild.draw(screen)

        Turn().draw(screen)

        if SquadDisplay().show and not Mapa().move_flag is None:
            SquadDisplay().display(Mapa().move_flag, screen)
        if KoniecGry().show:
            KoniecGry().draw(screen)
        MouseDisplay().draw(screen)
        AnimationMenager.display(screen)

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

                SideMenu().event(mouse_pos)
                Mapa().event(
                    mouse_pos,
                    self.squadButtonDisplay,
                    self.rotateButton,
                    self.wzmocnienieButton,
                    self.inzynierButton,
                    self.inzynierBuild,
                    SideMenu().dirty,
                    SideMenu().reset,
                )

                Turn().event(mouse_pos)
                Resource().event(mouse_pos)
                if isinstance(Mapa().move_flag, Squad):
                    self.squadButtonDisplay.event(mouse_pos, Mapa().move_flag)
                    self.rotateButton.event(
                        Mapa().move_flag, mouse_pos, Client().player.id
                    )
                    self.wzmocnienieButton.event(
                        Mapa().move_flag, mouse_pos, Client().player.id
                    )
                    self.inzynierButton.event(
                        mouse_pos, Mapa().move_flag, self.inzynierBuild
                    )

                if SquadDisplay().show:
                    SquadDisplay().event(
                        mouse_pos, Mapa().move_flag, Client().player.id, Mapa()
                    )


if __name__ == "__main__":
    gra = Gra()
    gra.run()
