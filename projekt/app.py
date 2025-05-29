import pygame
from sys import exit
from os.path import join
from ustawienia import *  # plik z ustawieniami
from jednostki import Wojownik, Yukimura_Sanada as y


# klasa reprezentująca grę
class Gra:
    # inicjalizacja gry
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))  # okienko
        pygame.display.set_caption(Title)
        self.clock = pygame.time.Clock()

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
            (100, 500),
        )
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyjdź z programu
                    pygame.quit()
                    exit()

            self.screen.fill("blue")  # wypełnia screena na niebiesko
            w.marsz()
            if w.rect is not None:
                self.screen.blit(w.surf, w.rect)
            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się gra.run()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
