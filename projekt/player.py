import pygame


class Player:
    def __init__(self):
        self.name = "anonim"
        self._gold = 100000
        self.army_group = pygame.sprite.Group()

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
