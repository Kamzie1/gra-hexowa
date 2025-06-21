from .narzedzia import get_sasiedzi, id_to_pos
import random

Miasto = {
    "id": 0,  # miasto jednostka
    "kategoria": "specjalne",
    "zdrowie": 500,
    "morale": 90,
}

starting_state = {"jednostki": [], "budynki": []}

mapa = [[0 for _ in range(30)] for _ in range(30)]


def get_miasto(package, owner):
    return {
        "pos": id_to_pos(package["x"], package["y"]),
        "x": package["x"],
        "y": package["y"],
        "owner": owner,
        "owner_id": package["id"],
        "color": package["color"],
        "jednostki": [Miasto],
    }


def miasto_tile(x, y, miasto):
    return {
        "owner": miasto["owner"],
        "owner_id": miasto["owner_id"],
        "pos": id_to_pos(x, y),
        "color": miasto["color"],
        "id": 0,  # tile miasta
    }


def mark(x, y):
    sasiedzix, sasiedziy = get_sasiedzi(x, y)
    mapa[x][y] = 1
    for j in range(6):
        if x + sasiedzix[j] < 0 or x + sasiedzix[j] > 29:
            continue
        if y + sasiedziy[j] < 0 or y + sasiedziy[j] > 29:
            continue
        mapa[x + sasiedzix[j]][y + sasiedziy[j]] = 1


def generate_space(x, y):
    sasiedzix, sasiedziy = get_sasiedzi(x, y)
    mapa[x][y] = 1
    for i in range(6):
        if x + sasiedzix[i] < 0 or x + sasiedzix[i] > 29:
            continue
        if y + sasiedziy[i] < 0 or y + sasiedziy[i] > 29:
            continue
        mark(x + sasiedzix[i], y + sasiedziy[i])


def get_budynek_miasto(miasto):
    x = miasto["x"]
    y = miasto["y"]
    starting_state["budynki"].append(miasto_tile(x, y, miasto))
    sasiedzix, sasiedziy = get_sasiedzi(x, y)
    generate_space(x, y)
    for i in range(6):
        starting_state["budynki"].append(
            miasto_tile(x + sasiedzix[i], y + sasiedziy[i], miasto)
        )
        generate_space(x + sasiedzix[i], y + sasiedziy[i])


def get_wioska(x, y):
    return {
        "owner": "none",
        "owner_id": -1,
        "pos": id_to_pos(x, y),
        "color": "grey",
        "id": 1,  # tile wioski
    }


def generate_wioski(num):
    for _ in range(num):
        while True:
            x = random.randint(0, 29)
            y = random.randint(0, 29)
            if mapa[x][y] == 0:
                break
        starting_state["budynki"].append(get_wioska(x, y))
        generate_space(x, y)


def create_state(package1, user1, package2, user2):
    starting_state["jednostki"].append(get_miasto(package1, user1))
    starting_state["jednostki"].append(get_miasto(package2, user2))
    for miasto in starting_state["jednostki"]:
        get_budynek_miasto(miasto)
    generate_wioski(15)
    return starting_state
