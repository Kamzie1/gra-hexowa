import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, surf, pos, group, id, budynek=None, jednostka=None) -> None:
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.id = id
        self.budynek = budynek
        self.jednostka = jednostka
        self.hitbox_surf = pygame.Surface((112, 54))
        self.hitbox = self.hitbox_surf.get_frect(center=pos)
        self.pos = pos
