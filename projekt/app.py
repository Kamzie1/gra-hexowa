import pygame
from sys import exit
from os.path import join
from ustawienia import *  # plik z ustawieniami
from świat import Mapa, Mini_map, Resource, SideMenu
from player import Player


# klasa reprezentująca grę
class Gra:
    # inicjalizacja gry
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))  # okienko
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()
        self.track = False
        self.mapa = Mapa()
        self.mini_mapa = Mini_map()
        self.player = Player()
        self.resource = Resource()
        self.menu = SideMenu()

    # metoda uruchamiająca grę
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyjdź z programu
                    pygame.quit()
                    exit()
            # aktualizacja położenia mapy
            self.mapa.update()  # type: ignore pylance mi świruje i widzi to jako błąd, być może tak jest, ale na razie wszystko działa
            self.update_minimap()  # obsługa minimapy
            self.draw()  # rysuje wszystkie elementy

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS

    def update_minimap(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.mini_mapa.mapRect.collidepoint(mouse_pos):
                # jeżeli zachodzi interakcja z mini mapą, to licz współrzędne (odpowiednio zeskalowane)
                pos_y = mouse_pos[1] - mini_map_pos[1]
                pos_x = mouse_pos[0] + mini_width - mini_map_pos[0]
                mapa_pos_y = pos_y * skala
                mapa_pos_x = pos_x * skala
                self.mapa.origin = (-mapa_pos_x + srodek[0], -mapa_pos_y + srodek[1])  # type: ignore , srodek wyrównuje widok, przenosi origin o połowę wektora przekątnej ekranu
                self.mapa.mapRect = self.mapa.mapSurf.get_frect(
                    topleft=self.mapa.origin  # zaktualizuj położenie mapy
                )

    def draw(self):
        self.screen.fill("black")  # wypełnia screena
        self.draw_map()
        # self.draw_menu()
        self.draw_resource()
        self.draw_mini_map()

    def draw_map(self):
        self.screen.blit(self.mapa.mapSurf, self.mapa.mapRect)  # rysuje mapę
        self.mapa.tiles_group.draw(self.mapa.mapSurf)  # rysuje tilesy

    def draw_mini_map(self):
        self.mini_mapa.update()
        self.mini_mapa.origin = (  # type: ignore
            -self.mapa.origin[0] / skala,
            -self.mapa.origin[1] / skala,
        )
        self.mini_mapa.rect = self.mini_mapa.rectsurf.get_frect(
            topleft=self.mini_mapa.origin
        )
        pygame.draw.rect(
            self.mini_mapa.surf, mini_map_rect_color, self.mini_mapa.rect, width=1
        )
        self.screen.blit(
            self.mini_mapa.surf, self.mini_mapa.mapRect
        )  # rysuje mini mapę
        pygame.draw.rect(
            self.screen, (0, 0, 0), self.mini_mapa.mapRect, width=2
        )  # rysuje border
##nigger
    def draw_resource(self):
        self.screen.blit(self.resource.surf, self.resource.rect)
        self.resource.fill()
        self.resource.display_gold(self.player, (10, (resource_height - font_size) / 2))

    def draw_menu(self):
        self.menu.fill()
        self.screen.blit(self.menu.surf, self.menu.rect)


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
