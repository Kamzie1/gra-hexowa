import pygame
from sys import exit
from ustawienia import *  # plik z ustawieniami
from jednostki import Wojownik


class Gra:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width, Height))  # okienko
        pygame.display.set_caption("Gra")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyjdź z programu
                    pygame.quit()
                    exit()

            self.screen.fill("blue")  # wypełnia screena na niebiesko
            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się main()
if __name__ == "__main__":
    gra = Gra()
    gra.run()
