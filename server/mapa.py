from .mapy import mapy


def create_map(ustawienia):
    if ustawienia["mapa"] != "random":
        return mapy[ustawienia["mapa"]]
    else:
        width = ustawienia["width"]
        height = ustawienia["height"]
        rivers = ustawienia["rivers"]
        make_map(width, height, rivers)


def make_map(w, h, r):
    pass
