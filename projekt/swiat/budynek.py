import pygame
from os.path import join
from projekt.ustawienia import folder_grafiki


class Budynek(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface, name="Budynek"):
        super().__init__(group)
        self.pos = pos
        self.image = pygame.image.load(join(folder_grafiki, surface)).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.name = name
