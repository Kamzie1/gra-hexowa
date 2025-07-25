import pygame


class Player:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self._gold = 10000
        self.frakcja = data["frakcja"]
        self.pos = data["pos"]
        self.x = data["x"]
        self.y = data["y"]
        self.color = data["color"]
        self.zloto_income = 7 * self.frakcja["budynek"][0]["earn"]["gold"]
        self.akcje = data["akcje"]

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
