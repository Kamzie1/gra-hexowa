from .singleton import Singleton
import pygame
from projekt.assetMenager import AssetManager


class MouseDisplay(metaclass=Singleton):
    def __init__(self):
        self.show = False
        self.font = AssetManager.get_font("consolas", 16)
        self.display = ""

    def update(self, mouse_pos, display):
        self.display = display
        self.pos = mouse_pos
        self.show = True

    def draw(self, screen):
        if not self.show:
            return
        text = self.font.render(self.display, True, "white")
        text_rect = text.get_rect(bottomleft=self.pos)
        screen.blit(text, text_rect)
