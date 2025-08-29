import pygame
from projekt.akcjeMenager import AkcjeMenager
from projekt.assetMenager import AssetManager


class Player:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self._gold = 10000
        self.srebro = 10000
        self.stal = 10000
        self.medals = 10000
        self._food = 100000
        self.hunger = 0
        self.frakcja = data["frakcja"]
        self.pos = data["pos"]
        self.x = data["x"]
        self.y = data["y"]
        self.color = data["color"]
        self.income = {}
        self.akcjeMenager = AkcjeMenager(data["akcje"])

    @property
    def akcje(self):
        return self.akcjeMenager.buffs

    @property
    def gold(self):
        return self._gold

    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        if value < 0:
            self.hunger += 1
            self._food = 0
        else:
            self.hunger = 0
            self._food = value

    @gold.setter
    def gold(self, value):
        if value < 0:
            raise ValueError("no money")
        elif not isinstance(value, int):
            raise TypeError("wrong type")
        else:
            self._gold = value

    def earn(self):
        self.gold += self.income["zloto"]
        self.srebro += self.income["srebro"]
        self.stal += self.income["stal"]
        self.food += self.income["food"]

    def get_hunger_description(self):
        if self.hunger == 0:
            return "0 dni głodu"
        if self.hunger < 3:
            return f"{self.hunger} dni głodu \n -{self.hunger*2} do ruchu"
        else:
            return f"{self.hunger} dni głodu \n -4 do ruchu i -{self.hunger-2}% zdrowia"

    def __str__(self):
        return self.name
