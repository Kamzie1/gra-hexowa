from .narzedzia import get_sasiedzi, id_to_pos

Miasto = {
    "id": 0,  # miasto jednostka
    "kategoria": "specjalne",
    "zdrowie": 500,
    "morale": 90,
}

starting_state = {"jednostki": [], "budynki": []}


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


def get_budynek_miasto(miasto):
    x = miasto["x"]
    y = miasto["y"]
    starting_state["budynki"].append(miasto_tile(x, y, miasto))
    sasiedzix, sasiedziy = get_sasiedzi(x, y)
    for i in range(6):
        starting_state["budynki"].append(
            miasto_tile(x + sasiedzix[i], y + sasiedziy[i], miasto)
        )


def create_state(package1, user1, package2, user2):
    starting_state["jednostki"].append(get_miasto(package1, user1))
    starting_state["jednostki"].append(get_miasto(package2, user2))
    for miasto in starting_state["jednostki"]:
        get_budynek_miasto(miasto)
    return starting_state
