from projekt.jednostki import Wojownik


def test_inicjalizacje_klasy():
    w = Wojownik(100, 50, 12, 5, 3, 7, 3)
    assert w.zdrowie == 100
    assert w.morale == 50
    assert w.ruch == 12
    assert w.przebicie == 5
    assert w.pancerz == 3
    assert w.atak == 7
    assert w.koszt_ataku == 3


def test_printa():
    w = Wojownik(50, 20, 12, 5, 3, 7, 3)
    output = str(w)
    assert "zdrowie: 50" in output
    assert "morale: 20" in output
    assert "ruch: 12" in output
    assert "przebicie: 5" in output
    assert "pancerz: 3" in output
    assert "atak: 7" in output
    assert "koszt_ataku: 3" in output
