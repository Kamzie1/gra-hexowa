import pygame
from projekt.ustawienia import folder_grafiki, font
from os.path import join
from projekt.assetMenager import AssetManager


class Input:

    def __init__(self, width, height, pos, color, font_color, message, font_size=24):
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_frect(topleft=pos)
        self.surf.fill(color)
        self.color = color
        self.font = AssetManager.get_font("consolas", font_size)
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

    def update(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
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


class IntInput(Input):
    def __init__(self, width, height, pos, color, font_color, message, font_size=24):
        super().__init__(width, height, pos, color, font_color, message, font_size)

    def draw(self, screen):
        self.surf.fill(self.color)
        if self.active:
            pygame.draw.rect(self.surf, "black", self.surf.get_rect(), 2)
        text = self.font.render(self.display, True, self.font_color)
        text_rect = text.get_rect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)

    def update(self, event, mouse_pos):
        self.dirty = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            self.dirty = True
            if event.key == pygame.K_BACKSPACE:
                self.display = self.display[:-1]
                if len(self.display) == 0:
                    self.display = "0"
            elif event.unicode.isdigit():
                self.display += event.unicode


class CheckBox:
    def __init__(self, width, height, pos, value=False):
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_frect(center=pos)
        self.value = value
        self.dirty = False

    def display(self, screen):
        if self.value:
            pygame.draw.rect(screen, "black", self.rect)
        else:
            pygame.draw.rect(screen, "black", self.rect, 2)

    def event(self, event, mouse_pos):
        self.dirty = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.dirty = True
                self.value = not self.value
