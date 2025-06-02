import pygame
from sys import exit
from os.path import join
from ustawienia import *  # plik z ustawieniami
from świat import Mapa, Mini_map, Resource, SideMenu
from player import Player
from math import sqrt
from narzedzia import *


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
        self.click_flag = False
        self.show = True
        self.menu = SideMenu(self.player, self.mapa)
        self.move_flag = None

    # metoda uruchamiająca grę
    def run(self):
        while True:
            self.event_handler()
            # aktualizacja położenia mapy
            self.mapa.update()
            self.mini_mapa.update_minimap(self.mapa)  # obsługa minimapy
            self.draw()  # rysuje wszystkie elementy

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS

    def draw(self):
        self.screen.fill("black")  # wypełnia screena
        self.draw_map()
        if self.show:
            self.draw_menu()
        self.draw_resource()
        self.draw_mini_map()
        self.player.army_group.draw(self.mapa.mapSurf)

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
        self.resource.button_group.draw(self.resource.surf)
        self.resource.display_gold(
            self.player, (200, (resource_height - font_size) / 2)
        )

    def draw_menu(self):
        # self.menu.fill()
        self.screen.blit(self.menu.surf, self.menu.rect)
        self.menu.surf.blit(self.menu.recruit_surface, self.menu.recruit_rec)

        self.menu.recruit_group.draw(self.menu.recruit_surface)

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
                if self.menu.rect.collidepoint(mouse_pos) and self.show:
                    mouse_pos = pozycja_myszy_na_surface(mouse_pos, menu_pos)
                    for button in self.menu.recruit_group:
                        if button.rect.collidepoint(mouse_pos):
                            print("button click")
                            button.click()
                elif self.resource.rect.collidepoint(mouse_pos):
                    mouse_pos = pozycja_myszy_na_surface(mouse_pos, resource_pos)
                    for button in self.resource.button_group:
                        if button.rect.collidepoint(mouse_pos):
                            self.show = button.click(self.show)
                            print("button click")
                else:
                    mouse_pos = pozycja_myszy_na_surface(mouse_pos, self.mapa.origin)

                    for tiles in self.mapa.Tile_array:
                        for tile in tiles:
                            if self.Clicked(tile.pos, mouse_pos):
                                if self.move_flag is None:
                                    print("clicked")
                                    self.move_flag = tile.jednostka
                                else:
                                    if tile.jednostka is None:
                                        print("move")
                                        self.move_flag.pos = tile.pos
                                        self.move_flag.tile.jednostka = None
                                        self.move_flag.tile = tile
                                        tile.jednostka = self.move_flag
                                        print(self.move_flag)
                                        print(tile.id, tile.jednostka)
                                    self.move_flag = None

                self.click_flag = False


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
