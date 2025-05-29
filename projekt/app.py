import pygame
from sys import exit
from os.path import join
from ustawienia import *  # plik z ustawieniami
from jednostki import Wojownik, Yukimura_Sanada as y
from świat import Mapa, Mini_map


# klasa reprezentująca grę
class Gra:
    # inicjalizacja gry
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))  # okienko
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()
        self.track = False

    # metoda uruchamiająca grę
    def run(self):
        w = Wojownik(
            y["zdrowie"],
            y["morale"],
            y["ruch"],
            y["przebicie"],
            y["pancerz"],
            y["atak"],
            y["koszt_ataku"],
            y["image"],
            (100, 100),
        )
        mapa = Mapa(3416, 1674, "grey", (400, 400))
        mini_map = Mini_map(200, 100, "blue", (Width, Height))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyjdź z programu
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    original_pos = event.pos
                    original_origin = mapa.origin
                    print(original_pos)
                    self.track = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.track = False
            if self.track == True:
                mouse_pos = pygame.mouse.get_pos()
                print("mouse: ", mouse_pos)
                offset = (
                    mouse_pos[0] - original_pos[0],
                    mouse_pos[1] - original_pos[1],
                )
                mapa.origin = (
                    original_origin[0] + offset[0],
                    original_origin[1] + offset[1],
                )
                print("origin: ", mapa.origin)

            mapa.update()

            self.screen.fill("black")  # wypełnia screena na niebiesko
            self.screen.blit(mapa.mapSurf, mapa.mapRect)
            mapa.fill()
            self.screen.blit(mini_map.mapSurf, mini_map.mapRect)
            mini_map.fill()

            w.marsz()
            if w.rect is not None:
                mapa.mapSurf.blit(w.surf, w.rect)
            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
