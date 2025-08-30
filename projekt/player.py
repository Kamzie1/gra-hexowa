import pygame
from projekt.akcjeMenager import AkcjeMenager
from projekt.assetMenager import AssetManager


class Player:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self._gold = data["gold"]
        self.srebro = data["srebro"]
        self.stal = data["stal"]
        self.medals = data["medals"]
        self.food = data["food"]
        self.team = data["team"]
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

    @akcje.setter
    def akcje(self, value):
        self.akcjeMenager.buffs = value

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
        if self.hunger < 4:
            return f"{self.hunger} dni głodu \n -{self.hunger*3} do ruchu"
        else:
            return f"{self.hunger} dni głodu \n -9 do ruchu i -{self.hunger-3}% zdrowia"

    def __str__(self):
        return self.name
