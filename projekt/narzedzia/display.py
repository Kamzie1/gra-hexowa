import pygame
from os.path import join
from projekt.assetMenager import AssetManager
from .mouseDisplay import MouseDisplay


class Display:
    def __init__(self, width, height, pos, font="consolas", font_size=26):
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))
        self.rect = self.surf.get_rect(topleft=pos)
        self.font = AssetManager.get_font(font, font_size)

    def display(self, content, color, screen):

        self.surf.fill((0, 0, 0, 0))
        text = self.font.render(content, True, color)
        text_rect = text.get_frect(topleft=(5, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)


class TurnDisplay(Display):
    def __init__(self, width, height, pos, font, font_size):
        super().__init__(width, height, pos, font, font_size)

    def display(self, color, screen, users, turn, pogoda, forecast):
        text = f"{users[turn % len(users)]["name"]}"
        content = (
            f"{turn//len(users) +1}     "
            + text
            + "   "
            + AssetManager.typyPogodyNazwa[pogoda[0]]
        )
        if forecast:
            content = content + " | " + AssetManager.typyPogodyNazwa[pogoda[1]]
        super().display(content, color, screen)

    def hover(self, mouse_pos, pogoda, forecast):
        if self.rect.collidepoint(mouse_pos):
            if forecast:
                MouseDisplay().update(
                    mouse_pos,
                    AssetManager.typyPogodyOpis[pogoda[0]]
                    + " | "
                    + AssetManager.typyPogodyOpis[pogoda[1]],
                )
            else:
                MouseDisplay().update(mouse_pos, AssetManager.typyPogodyOpis[pogoda[0]])
