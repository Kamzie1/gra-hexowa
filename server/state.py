from .narzedzia import get_sasiedzi, id_to_pos
import random

Miasto = {
    "id": 0,  # miasto jednostka
    "kategoria": "specjalne",
    "zdrowie": 500,
    "morale": 90,
}


def get_miasto_jednostka(client, x, y):
    return {
        "pos": id_to_pos(x, y),
        "x": x,
        "y": y,
        "owner": client["name"],
        "owner_id": client["id"],
        "color": client["color"],
        "jednostki": [Miasto],
    }


def miasto_tile(x, y, user):
    return {
        "owner": user["name"],
        "owner_id": user["id"],
        "pos": id_to_pos(x, y),
        "color": user["color"],
        "id": 0,  # tile miasta
    }


def get_budynek_miasto(user, positions, starting_state):
    x = user["x"]
    y = user["y"]
    starting_state["budynki"].append(miasto_tile(x, y, user))
    sasiedzix, sasiedziy = get_sasiedzi(x, y)
    for i in range(6):
        starting_state["budynki"].append(
            miasto_tile(x + sasiedzix[i], y + sasiedziy[i], user)
        )
        positions.append((x + sasiedzix[i], y + sasiedziy[i]))


def get_wioska(x, y):
    return {
        "owner": "none",
        "owner_id": -1,
        "pos": id_to_pos(x, y),
        "color": "grey",
        "id": 1,  # tile wioski
    }


def generate_wioski(num, positions, starting_state):
    space = 4**2
    max_powtorzen = 1000
    for _ in range(num):
        powtorzenie = 0
        x = 0
        y = 0
        flag = False
        while True:
            flag = True
            x = 1 + random.randint(0, 27)
            y = 1 + random.randint(0, 27)
            powtorzenie += 1
            if powtorzenie > max_powtorzen:
                return
            for pos in positions:
                if odl(x, y, pos[0], pos[1]) < space:
                    flag = False
                    break
            if flag:
                break

        positions.append((x, y))
        starting_state["budynki"].append(get_wioska(x, y))


def odl(x, y, x1, y1):
    return (x - x1) ** 2 + (y - y1) ** 2


def get_miasto(user, positions):
    space = 10**2
    powtorzenie = 0
    max_powtorzen = 1000
    x = 0
    y = 0
    flag = False
    while True:
        flag = True
        x = 4 + random.randint(0, 21)
        y = 4 + random.randint(0, 21)
        powtorzenie += 1
        for pos in positions:
            if odl(x, y, pos[0], pos[1]) < space:
                flag = False
                break
        if powtorzenie > max_powtorzen:
            flag = True
            print("za mało miejsca")
        if flag:
            break

    user["x"] = x
    user["y"] = y
    positions.append((x, y))
    return get_miasto_jednostka(user, x, y)


def create_state(users, ustawienia):
    starting_state = {"jednostki": [], "budynki": []}
    pos = []
    for user in users:
        print(user)
        user["gold"] = 1000
        starting_state["jednostki"].append(get_miasto(user, pos))
        get_budynek_miasto(user, pos, starting_state)
    generate_wioski(ustawienia["wioski"], pos, starting_state)
    return starting_state
