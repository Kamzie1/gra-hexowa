from projekt.ustawienia import *
from projekt.narzedzia import pozycja_myszy_na_surface
from os.path import join
import pygame
from .buttons import Menu, Surrender
from projekt.assetMenager import AssetManager
from projekt.narzedzia import Singleton, KoniecGry
from projekt.network import Client
from .mapa import Mapa
from .mouseDisplay import MouseDisplay


class Resource(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.surf = pygame.Surface((resource_width, resource_height), pygame.SRCALPHA)
        self.fill()
        self.rect = self.surf.get_frect(topleft=resource_pos)
        self.font = AssetManager.get_font("consolas", 16)
        self.button_group = pygame.sprite.Group()
        Menu(50, 50, "blue", (10, 0), self.button_group, "schowaj sidepanel")
        Surrender(50, 50, "yellow", (70, 0), self.button_group, "poddaj się")

    def fill(self):
        self.surf.fill(resource_color)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.button_group:
            if button.rect.collidepoint(mouse_pos):
                button.hover()
                MouseDisplay().update(mouse_pos, button.description)

    def display(self, player):
        # icon
        gold = AssetManager.get_asset("zloto")
        srebro = AssetManager.get_asset("srebro")
        stal = AssetManager.get_asset("stal")
        medals = AssetManager.get_asset("medale")
        food = AssetManager.get_asset("food")
        rect = srebro.get_frect(center=(150, resource_height / 2))
        self.surf.blit(srebro, rect)
        rect = stal.get_frect(center=(325, resource_height / 2))
        self.surf.blit(stal, rect)
        rect = gold.get_frect(center=(500, resource_height / 2))
        self.surf.blit(gold, rect)
        rect = food.get_frect(center=(675, resource_height / 2))
        self.surf.blit(food, rect)
        rect = medals.get_frect(center=(850, resource_height / 2))
        self.surf.blit(medals, rect)
        # number
        display = f"{player.srebro} (+{player.income["srebro"]})"
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=(175, (resource_height - font_size) / 2))
        self.surf.blit(text, text_rect)
        display = f"{player.stal} (+{player.income["stal"]})"
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=(350, (resource_height - font_size) / 2))
        self.surf.blit(text, text_rect)
        display = f"{player.gold} (+{player.income["zloto"]})"
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=(525, (resource_height - font_size) / 2))
        self.surf.blit(text, text_rect)
        display = f"{player.food} (+{player.income["food"]})"
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=(700, (resource_height - font_size) / 2))
        self.surf.blit(text, text_rect)
        display = f"{player.medals}"
        text = self.font.render(display, True, font_color)
        text_rect = text.get_rect(topleft=(875, (resource_height - font_size) / 2))
        self.surf.blit(text, text_rect)

    def event(self, mouse_pos, flag):
        if self.rect.collidepoint(mouse_pos):
            flag.klikniecie_flag = False
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, resource_pos)
            for button in self.button_group:
                if button.rect.collidepoint(mouse_pos):
                    if isinstance(button, Menu):
                        button.click(flag)
                    else:
                        button.click()

    def draw(self, screen):
        self.fill()
        self.display(Client().player)
        self.button_group.draw(self.surf)
        screen.blit(self.surf, self.rect)
