tile_width = 112
tile_height = 108


def id_to_pos(x, y):
    if y % 2 == 0:
        pos = (
            x * tile_width + tile_width / 2,
            y * tile_height / 4 * 3 + tile_height / 2,
        )
    else:
        pos = (
            x * tile_width + tile_width,
            y * tile_height / 4 * 3 + tile_height / 2,
        )
    return pos


Miasto1 = {
    "id": "miasto",
    "pos": id_to_pos(6, 6),
    "owner": "client2",
    "owner_id": 1,
    "color": "red",
    "zdrowie": 1000,
    "morale": 90,
}

Miasto2 = {
    "id": "miasto",
    "pos": id_to_pos(24, 24),
    "owner": "client1",
    "owner_id": 0,
    "color": "blue",
    "zdrowie": 1000,
    "morale": 90,
}

starting_state = {"jednostka": [], "budynek": [Miasto1, Miasto2]}
