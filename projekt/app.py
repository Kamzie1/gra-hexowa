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
        mapa = Mapa(Mapa_width, Mapa_height, (0, 0))
        mini_map = Mini_map(mini_width, mini_height, "blue", (Width, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyjdź z programu
                    pygame.quit()
                    exit()
                # poruszanie się po mapie
                if event.type == pygame.MOUSEBUTTONDOWN:
                    original_pos = event.pos
                    original_origin = mapa.origin
                    self.track = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.track = False
            # aktualizacja położenia mapy
            if self.track:
                mapa.update(original_origin, original_pos)  # type: ignore pylance mi świruje i widzi to jako błąd, być może tak jest, ale na razie wszystko działa

            self.screen.fill("black")  # wypełnia screena
            self.screen.blit(mapa.mapSurf, mapa.mapRect)  # rysuje mapę
            mapa.tiles_group.draw(mapa.mapSurf)  # rysuje tilesy
            self.screen.blit(mini_map.mapSurf, mini_map.mapRect)  # rysuje mini mapę
            mini_map.fill()  # odświeża minimapę

            w.marsz()  # marsz Yukimury
            mapa.mapSurf.blit(w.surf, w.rect)  # type: ignore
            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
