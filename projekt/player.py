import pygame
from projekt.jednostki import get_fraction
from projekt.narzedzia import id_to_pos


class Player:
    def __init__(self, user):
        self.id = user["id"]
        self.name = user["name"]
        self._gold = user["gold"]
        self.frakcja = get_fraction(user["fraction"])
        self.recruit_pos = id_to_pos(user["x"], user["y"])
        self.x = user["x"]
        self.y = user["y"]
        self.color = user["color"]

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
