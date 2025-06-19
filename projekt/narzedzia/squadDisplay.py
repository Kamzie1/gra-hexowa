import pygame
from os.path import join


class SquadDisplay:
    def __init__(self, width, height, pos, color):
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_frect(center=pos)
        self.font = pygame.font.Font("Grafika/consolas.ttf", 24)
        self.font_color = color
        self.show = False

    def display(self, squad, screen):
        self.surf.fill("white")
        self.display_wojownik(squad, (5, 5), 0)
        y = 55
        i = 1
        for wojownik in squad.wojownicy:
            self.display_wojownik(wojownik, (5, y), i)
            y += 50
            i += 1
        screen.blit(self.surf, self.rect)

    def display_wojownik(self, wojownik, pos, id):
        display = wojownik.display(id)
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=pos)
        self.surf.blit(text, text_rect)
