import pygame
from os.path import join


class Display:
    def __init__(self, width, height, pos, font, font_size):
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))
        self.rect = self.surf.get_rect(topleft=pos)
        self.font = pygame.font.Font(join("Grafika/fonts", font), font_size)

    def display(self, content, color, screen):

        self.surf.fill((0, 0, 0, 0))
        text = self.font.render(content, True, color)
        text_rect = text.get_frect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)


class TurnDisplay(Display):
    def __init__(self, width, height, pos, font, font_size):
        super().__init__(width, height, pos, font, font_size)

    def display(self, color, screen, turn, users):
        if len(users) == 0:
            text = "Koniec Gry"
            content = f"{turn +1}     " + text
        else:
            text = f"{users[turn % len(users)]["name"]}"
            content = f"{turn//len(users) +1}     " + text
        super().display(content, color, screen)
