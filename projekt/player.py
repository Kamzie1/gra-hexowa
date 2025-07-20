import pygame


class Player:
    def __init__(self, Frakcja, pos, x, y, id, name, color):
        self.id = id
        self.name = name
        self._gold = 100000
        self.frakcja = Frakcja
        self.recruit_pos = pos
        self.x = x
        self.y = y
        self.color = color
        self.zloto_income = 7 * self.frakcja["budynek"][0]["earn"]["gold"]

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

    def __str__(self):
        return self.name
