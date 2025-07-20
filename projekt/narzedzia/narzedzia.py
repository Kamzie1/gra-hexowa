from ..ustawienia import tile_height, tile_width
from math import sqrt


def oblicz_pos(x, y):
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


def pozycja_myszy_na_surface(mouse_pos, origin):
    return (
        mouse_pos[0] - origin[0],
        mouse_pos[1] - origin[1],
    )


def clicked(pos, mouse_pos) -> bool:
    r = sqrt(3) * tile_height / 4
    a, b = pos
    if pow(mouse_pos[0] - a, 2) + pow(mouse_pos[1] - b, 2) <= pow(r, 2):
        return True
    return False


def oslab_kolor(color, value):
    r = color.r
    g = color.g
    b = color.b

    return (r, g, b, value)


# tablica sąsiadów
sasiedzi1x = [-1, 0, 0, 1, 1, 1]

sasiedzi1y = [0, 1, -1, 0, 1, -1]

sasiedzi2x = [1, 0, 0, -1, -1, -1]

sasiedzi2y = [0, 1, -1, 0, 1, -1]


def get_sasiedzi(x, y):
    match (y % 2):
        case 1:
            return (sasiedzi1x, sasiedzi1y)
        case 0:
            return (sasiedzi2x, sasiedzi2y)


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


def calc_scaled_offset(offset, pos, skala):
    return (pos[0] + offset[0] * skala, pos[1] + offset[1] * skala)
