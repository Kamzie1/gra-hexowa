import pygame


class Player:
    def __init__(self, Frakcja, pos, x, y, id, name="anonim"):
        self.id = id
        self.name = name
        self._gold = 100000
        self.army_group = pygame.sprite.Group()
        self.frakcja = Frakcja
        self.recruit_pos = pos
        self.x = x
        self.y = y

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        if value < 0:
            raise ValueError("no money")
        elif not isinstance(value, int):
            raise TypeError("wrong type")
        else:
            self._gold = value
