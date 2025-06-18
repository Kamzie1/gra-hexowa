import pygame
from projekt.ustawienia import folder_grafiki, font
from os.path import join


class Input:

    def __init__(self, width, height, pos, color, font_color, message):
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_frect(topleft=pos)
        self.surf.fill(color)
        self.color = color
        self.font = pygame.font.Font(join(folder_grafiki, font), 24)
        self.font_color = font_color
        self.message = message
        self._display = message
        self.active = False

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):

        self._display = value
        self.surf.fill(self.color)
        text = self.font.render(self.display, True, self.font_color)
        text_rect = text.get_rect(topleft=(5, 5))
        self.surf.blit(text, text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.display = self.display[:-1]
            else:
                self.display += event.unicode

    def draw(self, screen):
        self.surf.fill(self.color)
        if self.active:
            pygame.draw.rect(self.surf, "black", self.surf.get_rect(), 2)
            if self.display == self.message:
                self.display = ""
        elif not self.active and self.display == "":
            self.display = self.message
        text = self.font.render(self.display, True, self.font_color)
        text_rect = text.get_rect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
