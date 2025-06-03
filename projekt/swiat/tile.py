import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, surf, x, y, pos, group, id, koszt_ruchu, typ, budynek=None, jednostka=None
    ) -> None:
        super().__init__(group)
        self.x = x
        self.y = y
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.id = id
        self.budynek = budynek
        self.jednostka = jednostka
        self.hitbox_surf = pygame.Surface((112, 54))
        self.hitbox = self.hitbox_surf.get_frect(center=pos)
        self.pos = pos
        self.koszt_ruchu = koszt_ruchu
        self.typ = typ


class Najechanie:
    def __init__(self, surf, pos):
        self._origin = pos
        self.image = surf
        self.rect = self.image.get_frect(center=self.origin)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = self.image.get_frect(center=self.origin)


class Ruch(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self._origin = pos
        self.image = surf
        self.rect = self.image.get_frect(center=self.origin)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        self.rect = self.image.get_frect(center=self.origin)
