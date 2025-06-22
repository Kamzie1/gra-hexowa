from projekt.swiat import Mapa
import pygame


def create_test_unit(positions):
    tablica = [[0 for _ in range(30)] for _ in range(30)]
    for x, y in positions:
        tablica[x][y] = 1
    return tablica


def init():
    pygame.display.init()
    pygame.display.set_mode((1, 1))  # potrzebne do convert_alpha()

    mapa = Mapa()
    for tiles in mapa.Tile_array:
        for tile in tiles:
            tile.koszt_ruchu = 3
    return mapa


def test_possible_moves():
    mapa = init()
    assert mapa.possible_moves(0, 0, 3) == create_test_unit([(0, 0), (1, 0), (0, 1)])
    assert mapa.possible_moves(0, 0, 5) == create_test_unit([(0, 0), (1, 0), (0, 1)])
    assert mapa.possible_moves(0, 0, 6) == create_test_unit(
        [(0, 0), (1, 0), (0, 1), (0, 2), (1, 1), (2, 0), (1, 2)]
    )
    assert mapa.possible_moves(0, 0, 1) == create_test_unit([(0, 0)])
