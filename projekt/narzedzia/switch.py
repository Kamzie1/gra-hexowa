import pygame
from projekt.assetMenager import AssetManager


class Switch:
    def __init__(self, width, height, pos, forms):
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_frect(topright=pos)
        self.forms = forms
        self.pos = pos
        self.font = AssetManager.get_font("consolas", 20)

    def draw(self, id, screen):
        self.surf.fill("white")
        display = self.font.render(self.forms[id], True, "black")
        display_rect = display.get_rect(topleft=(5, 5))
        self.surf.blit(display, display_rect)

        screen.blit(self.surf, self.rect)
