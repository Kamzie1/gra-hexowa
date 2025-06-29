import pygame
from projekt.ustawienia import folder_grafiki, font
from os.path import join


class Przycisk:
    def __init__(self, width, height, color, pos, tekst, font_color) -> None:
        self.surf = pygame.Surface((width, height))
        self.color = color
        self.surf.fill(color)
        self.pos = pos
        self.rect = self.surf.get_frect(topleft=self.pos)
        self.display = tekst
        self.font = pygame.font.Font(join("Grafika/fonts", font), 24)
        self.font_color = font_color

    def draw(self, screen):
        self.surf.fill(self.color)
        text = self.font.render(self.display, True, self.font_color)
        text_rect = text.get_rect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)


class PrzyciskReady(Przycisk):
    def __init__(self, width, height, color, pos, tekst, font_color):
        super().__init__(width, height, color, pos, tekst, font_color)
        self.value = 0
        self.displays = ["Gotowy", "Cancel"]
        self.rect = self.surf.get_frect(bottomright=pos)

    def click(self):
        self.value += 1
        self.value %= 2
        self.display = self.displays[self.value]


class Switch:
    def __init__(self, width, height, pos, forms):
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_frect(bottomright=pos)
        self.forms = forms
        self.pos = pos
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", 20)

    def draw(self, id, screen):
        self.surf.fill("white")
        display = self.font.render(self.forms[id], True, "black")
        display_rect = display.get_rect(topleft=(5, 5))
        self.surf.blit(display, display_rect)

        screen.blit(self.surf, self.rect)


class ColorSwitch(Switch):
    def __init__(self, width, height, pos, forms):
        super().__init__(width, height, pos, forms)
        self.rect = self.surf.get_frect(topleft=pos)

    def draw(self, id, screen):
        self.surf.fill(self.forms[id])
        screen.blit(self.surf, self.rect)
