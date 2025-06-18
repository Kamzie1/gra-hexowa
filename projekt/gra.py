import pygame
from sys import exit
from projekt.ustawienia import *  # plik z ustawieniami
from projekt.swiat import Mapa, Mini_map, Resource, SideMenu, Turn
from projekt.player import Player
from projekt.narzedzia import oblicz_pos, TurnDisplay
from projekt.flag import Flag
from projekt.jednostki import get_fraction


class Gra:
    def __init__(self, client):
        name = client.names[0]
        name2 = client.names[1]
        x = client.info[name]["x"]
        y = client.info[name]["y"]
        frakcja = get_fraction(client.info[name]["frakcja"])
        num = client.info[name]["id"]
        pos = oblicz_pos(x, y)
        x2 = client.info[name2]["x"]
        y2 = client.info[name2]["y"]
        frakcja2 = get_fraction(client.info[name2]["frakcja"])
        num2 = client.info[name2]["id"]
        pos2 = oblicz_pos(x2, y2)
        # pygame
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(Title)
        # obiekty
        self.clock = pygame.time.Clock()
        self.mini_mapa = Mini_map(pos)
        self.player = Player(frakcja, pos, x, y, num, name, client.info[name]["color"])
        self.opponent = Player(
            frakcja2, pos2, x2, y2, num2, name2, client.info[name2]["color"]
        )
        self.mapa = Mapa(pos, x, y, self.player, self.opponent, client.state)
        self.resource = Resource()
        self.turn = Turn()
        self.menu = SideMenu(self.player, self.mapa)
        self.flag = Flag()
        self.client = client
        client.mapa = self.mapa
        client.user = self.player.name
        client.id = self.player.id
        self.turn_display = TurnDisplay(
            300, 34, (srodek[0] - 25, 0), "consolas.ttf", 20
        )

    # metoda uruchamiająca grę
    def run(self):
        while True:
            if not self.client.state_loaded:
                self.clock.tick(FPS)
                continue

            self.event_handler()

            self.update()
            self.draw()  # rysuje wszystkie elementy

            pygame.display.update()

            self.clock.tick(FPS)

    def update(self):
        self.mapa.update()
        self.mini_mapa.update(self.mapa)

    def draw(self):
        self.screen.fill("black")
        self.mapa.draw(self.screen, self.flag)
        if self.flag.show:
            self.menu.draw(self.screen)
        self.resource.draw(self.screen, self.player)
        self.turn_display.display(
            "grey", self.screen, self.client.turn, self.player, self.opponent
        )
        self.mini_mapa.draw(self.screen, self.mapa.origin, self.mapa.Tile_array)
        for jednostka in self.mapa.army_group:
            jednostka.draw(self.mapa.mapSurf)

        self.turn.draw(self.screen)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                self.mapa.event(mouse_pos, self.flag, self.client.turn, self.client.id)
                self.turn.event(mouse_pos, self.mapa, self.client)
                self.resource.event(mouse_pos, self.flag)
                self.menu.event(mouse_pos, self.flag, self.client.turn, self.client.id)


if __name__ == "__main__":

    client = Client()
    client.start_game(client.uruchom_gre())
    gra = Gra(client)
    gra.run()
