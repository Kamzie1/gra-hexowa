from projekt.ustawienia import *
from projekt.narzedzia import pozycja_myszy_na_surface
from os.path import join
import pygame
from .buttons import Menu, Surrender


class Resource:
    def __init__(self):
        self.surf = pygame.Surface((resource_width, resource_height), pygame.SRCALPHA)
        self.fill()
        self.rect = self.surf.get_frect(topleft=resource_pos)
        self.font = pygame.font.Font(join("Grafika/fonts", font), font_size)
        self.button_group = pygame.sprite.Group()
        Menu(
            50,
            50,
            "blue",
            (10,0),
            self.button_group,
        )
        Surrender(50, 50, "yellow", (70, 0), self.button_group)

    def fill(self):
        self.surf.fill(resource_color)

    def display_gold(self, player, pos):
        # icon
        image = pygame.image.load(join("grafika", "złoto.png"))
        rect = image.get_frect(topleft=(150, (resource_height - font_size) / 2))
        self.surf.blit(image, rect)
        # number
        display = f"{player.gold} "
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=pos)
        self.surf.blit(text, text_rect)

    def event(self, mouse_pos, flag, client, koniecGry):
        if self.rect.collidepoint(mouse_pos):
            flag.klikniecie_flag = False
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, resource_pos)
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    if isinstance(button, Menu):
                        button.click(flag)
                    else:
                        button.click(client, koniecGry)

    def draw(self, screen, player):
        self.fill()
        self.display_gold(player, (200, (resource_height - font_size) / 2))
        self.button_group.draw(self.surf)
        screen.blit(self.surf, self.rect)
