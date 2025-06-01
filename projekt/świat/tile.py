import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group, id, object) -> None:
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.id = id
        self.object = object
