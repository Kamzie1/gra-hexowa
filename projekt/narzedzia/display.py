import pygame
from os.path import join
from projekt.assetMenager import AssetManager


class Display:
    def __init__(self, width, height, pos, font, font_size):
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))
        self.rect = self.surf.get_rect(topleft=pos)
        self.font = AssetManager.get_font("consolas", 26)

    def display(self, content, color, screen):

        self.surf.fill((0, 0, 0, 0))
        text = self.font.render(content, True, color)
        text_rect = text.get_frect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        pygame.draw.rect(self.surf, "red", self.rect, 2)
        screen.blit(self.surf, self.rect)


class TurnDisplay(Display):
    def __init__(self, width, height, pos, font, font_size):
        super().__init__(width, height, pos, font, font_size)

    def display(self, color, screen, turn, player, opponent):
        if turn % 2 == 0:
            if player.id == 0:
                text = f"{player.name}"
            else:
                text = f"{opponent.name}"
        else:
            if player.id == 1:
                text = f"{player.name}"
            else:
                text = f"{opponent.name}"
        content = f"{turn//2 +1}     " + text
        super().display(content, color, screen)
