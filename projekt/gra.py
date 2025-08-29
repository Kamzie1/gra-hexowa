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
    MouseDisplay,
    AttackDisplay,
    Wzmocnienie,
)
from projekt.player import Player
from projekt.narzedzia import (
    oblicz_pos,
    TurnDisplay,
    KoniecGry,
)
from projekt.flag import Flag
from projekt.network import Client
from .assetMenager import AssetManager
from .animationMenager import AnimationMenager


class Gra:
    def __init__(self):
        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(Title)
        AssetManager.preload_assets()
        Client().start_game(Client().uruchom_gre())
        # obiekty
        self.clock = pygame.time.Clock()
        Mini_map()
        AttackDisplay(Width / 1.2, Height / 1.2, srodek, "black")
        Mapa("mapa1(30x30)")
        Resource()
        Turn()
        SideMenu()
        self.flag = Flag()
        KoniecGry(Width, Height)
        self.turn_Display = TurnDisplay(
            300, 34, (srodek[0] - 25, 0), "consolas.ttf", 20
        )
        SquadDisplay(Width / 2, Height / 2, srodek, "black")
        self.squadButtonDisplay = SquadButtonDisplay(
            80, 80, "blue", (srodek[0] - 50, Height - 50)
        )
        self.rotateButton = Rotate(80, 80, "red", (srodek[0] + 50, Height - 50))
        self.wzmocnienieButton = Wzmocnienie(
            80, 80, "blue", (srodek[0] + 150, Height - 50)
        )

    # metoda uruchamiająca grę
    def run(self):
        while True:
            self.update()  # mouse hover

            self.event_handler()  # event (kliknięcie)

            self.draw()  # rysowanie

            pygame.display.update()

            self.clock.tick(FPS)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        MouseDisplay().show = False
        SideMenu().update(self.flag)
        Resource().update()
        if Mapa().Tile_array[Client().player.x][Client().player.y].jednostka is None:
            Client().end_game(-1)
        if (
            Mapa().Tile_array[Client().opponent.x][Client().opponent.y].jednostka
            is None
        ):
            Client().end_game(1)
        if SquadDisplay().show:
            SquadDisplay().update(pygame.mouse.get_pos())

        if Mapa().move_flag is not None:
            if self.squadButtonDisplay.rect.collidepoint(mouse_pos):
                MouseDisplay().update(mouse_pos, "Statystyki oddziału")

            if self.rotateButton.rect.collidepoint(mouse_pos):
                MouseDisplay().update(mouse_pos, "Obróć oddział")

            if self.wzmocnienieButton.rect.collidepoint(mouse_pos):
                MouseDisplay().update(
                    mouse_pos, "Wzmocnij oddział (+5% obrony) za 4 ruchu"
                )

        if AttackDisplay().show:
            AttackDisplay().hover(pygame.mouse.get_pos())

        Mapa().update()
        Mini_map().update()
        AnimationMenager.update()

    def draw(self):
        self.screen.fill("black")
        Mapa().draw(self.screen, self.flag)
        if self.flag.show:
            SideMenu().draw(self.screen)
        Resource().draw(self.screen)
        self.turn_Display.display(
            "grey", self.screen, Client().player, Client().opponent, Client().turn
        )
        Mini_map().draw(self.screen)
        for jednostka in Mapa().army_group:
            jednostka.draw(Mapa().mapSurf)

        if not Mapa().move_flag is None:
            self.screen.blit(
                self.squadButtonDisplay.image, self.squadButtonDisplay.rect
            )
            if Client().player.id == Mapa().move_flag.owner_id:
                self.screen.blit(self.rotateButton.image, self.rotateButton.rect)
                self.screen.blit(
                    self.wzmocnienieButton.image, self.wzmocnienieButton.rect
                )
        if AttackDisplay().show:
            AttackDisplay().display(self.screen)

        Turn().draw(self.screen)

        if SquadDisplay().show and not Mapa().move_flag is None:
            SquadDisplay().display(Mapa().move_flag, self.screen)
        if KoniecGry().show:
            KoniecGry().draw(self.screen)
        MouseDisplay().draw(self.screen)
        AnimationMenager.display(self.screen)

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

                SideMenu().event(mouse_pos, self.flag)
                Mapa().event(
                    mouse_pos,
                    self.flag,
                    self.squadButtonDisplay,
                    self.rotateButton,
                    SideMenu().dirty,
                    SideMenu().reset,
                )

                Turn().event(mouse_pos)
                Resource().event(mouse_pos, self.flag)
                self.squadButtonDisplay.event(mouse_pos, Mapa().move_flag)
                self.rotateButton.event(Mapa().move_flag, mouse_pos, Client().player.id)
                self.wzmocnienieButton.event(
                    Mapa().move_flag, mouse_pos, Client().player.id
                )

                if SquadDisplay().show:
                    SquadDisplay().event(
                        mouse_pos, Mapa().move_flag, Client().player.id, Mapa()
                    )


if __name__ == "__main__":
    gra = Gra()
    gra.run()
