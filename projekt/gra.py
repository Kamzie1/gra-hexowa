import pygame
from sys import exit
from os.path import join
from projekt.ustawienia import *  # plik z ustawieniami
from projekt.swiat import Mapa, Mini_map, Resource, SideMenu, Turn
from projekt.player import Player
from projekt.narzedzia import *
from projekt.flag import Flag
from projekt.jednostki import Japonia


# klasa reprezentująca grę
class Gra:
    # inicjalizacja gry
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        id1,
        id2,
        name="anonim",
        Frakcja1=Japonia,
        Frakcja2=Japonia,
    ):
        pos1 = oblicz_pos(x1, y1)
        pos2 = oblicz_pos(x1, y1)
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # okienko
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()
        self.mapa = Mapa(pos1, x1, y1)
        self.mini_mapa = Mini_map(pos1)
        self.player = Player(Frakcja1, pos1, x1, y1, id1, name)
        self.oponent = Player(Frakcja2, pos2, x2, y2, id2)
        self.resource = Resource()
        self.turn = Turn()
        self.menu = SideMenu(self.player, self.mapa)
        self.flag = Flag()

    # metoda uruchamiająca grę
    def run(self):
        while True:
            self.event_handler()

            self.update()
            self.draw()  # rysuje wszystkie elementy

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS

    def update(self):
        self.mapa.update()
        self.mini_mapa.update(self.mapa)

    def draw(self):
        self.screen.fill("black")  # wypełnia screena
        self.mapa.draw(
            self.screen,
            self.flag,
        )
        if self.flag.show:
            self.menu.draw(self.screen)
        self.resource.draw(self.screen, self.player)
        self.mini_mapa.draw(self.screen, self.mapa.origin)
        self.player.army_group.draw(self.mapa.mapSurf)
        self.turn.draw(self.screen)

    ##nigger

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wyjdź z programu
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                self.turn.event(mouse_pos, self.player.army_group)
                self.menu.event(mouse_pos, self.flag)
                self.resource.event(mouse_pos, self.flag)
                self.mapa.event(mouse_pos, self.flag)


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    x1 = 6
    y1 = 6
    x2 = 6
    y2 = 6
    gra = Gra(
        x1,
        y1,
        x2,
        y2,
        1,
        2,
    )
    gra.run()
