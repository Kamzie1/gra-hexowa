from ..ustawienia import tile_height, tile_width
from math import sqrt


def oblicz_id(origin, mouse_pos):
    pass


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


def oblicz_pos_screen(x, y, origin):
    pass


def clicked(pos, mouse_pos) -> bool:
    r = sqrt(3) * tile_height / 4
    a, b = pos
    if pow(mouse_pos[0] - a, 2) + pow(mouse_pos[1] - b, 2) <= pow(r, 2):
        return True
    return False
