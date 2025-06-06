from projekt.gra import Gra
from projekt.jednostki import Japonia
from projekt.narzedzia import oblicz_pos, Input, Przycisk
from projekt.ustawienia import FPS
import pygame


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))  # okienko
        pygame.display.set_caption("Main")
        self.screen.fill("white")
        self.clock = pygame.time.Clock()
        self.name_input = Input(
            300, 34, (100, 100), "grey", "black", "podaj swoje imię:"
        )
        self.id_input = Input(300, 34, (100, 150), "grey", "black", "wpisz id pokoju:")
        self.join = Przycisk(70, 34, "blue", (450, 150), "Join", "grey")
        self.create = Przycisk(200, 34, "green", (100, 200), "stwórz pokój", "black")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # wyjdź z programu
                    pygame.quit()
                    exit()
                else:
                    self.name_input.update(event)
                    self.id_input.update(event)
                    self.join.update(event)
                    self.create.update(event)

            self.name_input.draw(self.screen)
            self.id_input.draw(self.screen)
            self.join.draw(self.screen)
            self.create.draw(self.screen)

            pygame.display.update()  # odświeża display

            self.clock.tick(FPS)  # maks 60 FPS


if __name__ == "__main__":
    main = Main()
    main.run()
