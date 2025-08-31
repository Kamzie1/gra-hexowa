from .mapy import mapy
import random


def create_map(ustawienia):
    maps = ["mapa1(30x30)", "mapa2(10x10)", "mapa3(40x40)"]
    size = [(30, 30), (10, 10), (40, 40)]
    if ustawienia["mapa"] == "random":
        map_id = random.randint(0, len(maps) - 1)
        ustawienia["width"] = size[map_id][0]
        ustawienia["height"] = size[map_id][1]
        return mapy[maps[map_id]]
    elif ustawienia["mapa"] != "generuj":
        return mapy[ustawienia["mapa"]]
    else:
        width = ustawienia["width"]
        height = ustawienia["height"]
        rivers = ustawienia["rivers"]
        make_map(width, height, rivers)


def make_map(w, h, r):
    pass
