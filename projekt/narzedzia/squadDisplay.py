import pygame
from os.path import join
from .narzedzia import oslab_kolor


class SquadDisplay:
    def __init__(self, width, height, pos, color):
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_frect(center=pos)
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", int(self.width / 20))
        self.wojownik_font = pygame.font.Font(
            "Grafika/fonts/consolas.ttf", int(self.width / 40)
        )
        self.font_color = color
        self.show = False

    def display(self, squad, screen):
        self.surf.fill("white")
        self.display_wojownik(squad, (20, 20), 0, self.font)
        y = int(self.width / 20) * 2
        i = 1
        for wojownik in squad.wojownicy:
            self.display_wojownik(
                wojownik, (40, y + i * int(self.width / 20)), i, self.wojownik_font
            )
            i += 1
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, squad.color, self.rect, 4)

    def display_wojownik(self, wojownik, pos, id, font):
        display = wojownik.display(id)
        text = font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=pos)
        self.surf.blit(text, text_rect)
