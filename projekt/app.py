import pygame
from sys import exit
from os.path import join
from ustawienia import *  # plik z ustawieniami
from świat import Mapa, Mini_map, Resource, SideMenu
from player import Player
from jednostki import Yukimura_Sanada, Wojownik
from random import randint
from math import sqrt


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
        self.army_group = pygame.sprite.Group()
        self.click_flag = False
        self.menu = SideMenu(self.player, self.army_group)

    # metoda uruchamiająca grę
    def run(self):
        while True:
            self.event_handler()
            # aktualizacja położenia mapy
            self.mapa.update()
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
        self.draw_menu()
        self.draw_resource()
        self.draw_mini_map()
        self.army_group.draw(self.mapa.mapSurf)

    def draw_map(self):
        self.screen.blit(self.mapa.mapSurf, self.mapa.mapRect)  # rysuje mapę
        self.mapa.tiles_group.draw(self.mapa.mapSurf)  # rysuje tilesy
        self.mapa.building_group.draw(self.mapa.mapSurf)  # rysuje budynki

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
        # self.menu.fill()
        self.screen.blit(self.menu.surf, self.menu.rect)
        self.menu.button_group.draw(self.menu.surf)

    def Clicked(self, pos, mouse_pos) -> bool:
        r = sqrt(3) * tile_height / 4
        a, b = pos
        if pow(mouse_pos[0] - a, 2) + pow(mouse_pos[1] - b, 2) <= pow(r, 2):
            return True
        return False

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wyjdź z programu
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.click_flag = True
            elif event.type == pygame.MOUSEBUTTONUP and self.click_flag == True:
                mouse_pos = pygame.mouse.get_pos()
                if self.menu.rect.collidepoint(mouse_pos):
                    for button in self.menu.button_group:
                        mouse_pos = (
                            mouse_pos[0] - menu_pos[0],
                            mouse_pos[1] - menu_pos[1],
                        )
                        if button.rect.collidepoint(mouse_pos):
                            print("button click")
                            button.click()
                else:
                    mouse_pos = (
                        mouse_pos[0] - self.mapa.origin[0],
                        mouse_pos[1] - self.mapa.origin[1],
                    )

                    for tiles in self.mapa.Tile_array:
                        for tile in tiles:
                            if self.Clicked(tile.pos, mouse_pos):
                                print(f"kliknąłem heksa{tile.id}")
                self.click_flag = False


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
