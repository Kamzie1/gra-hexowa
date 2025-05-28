import pygame


def main():
    """
    główna pętla pygame
    """

    pygame.init()  # inicjalizacja pygame

    Width, Height = 600, 600
    screen = pygame.display.set_mode((Width, Height))  # okienko
    pygame.display.set_caption("Gra")
    clock = pygame.time.Clock()  # czaspy
    FPS = 60

    dziala = True
    while dziala:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # wyjdź z programu
                dziala = False

        screen.fill("blue")  # wypaełnia screena na niebiesko
        pygame.display.flip()  # odświeża display

        clock.tick(FPS)  # maks 60 FPS


# ważne!!! Odpala tylko, jeżeli został uruchomiony sam z siebie, a nie w formie zainportowanego modułu. Bez tego, gdybyśmy importwali ten program to przy imporcie uruchamiałby się main()
if __name__ == "__main__":
    main()
