tile_width = 112
tile_height = 108

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
