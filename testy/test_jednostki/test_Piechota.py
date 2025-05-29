from projekt.jednostki import Piechota

# test klasy Piechota dziedzica klasy Wojownik


# test inicjalizacji klasy
def test_inicjalizacje_klasy():
    p = Piechota(100, 50, 12, 5, 3, 7, 3)
    assert p.zdrowie == 100
    assert p.morale == 50
    assert p.ruch == 12
    assert p.przebicie == 5
    assert p.pancerz == 3
    assert p.atak == 7
    assert p.koszt_ataku == 3


# test wypisu informacji na temat jednostki
def test_printa():
    p = Piechota(50, 20, 12, 5, 3, 7, 3)
    output = str(p)
    assert "zdrowie: 50" in output
    assert "morale: 20" in output
    assert "ruch: 12" in output
    assert "przebicie: 5" in output
    assert "pancerz: 3" in output
    assert "atak: 7" in output
    assert "koszt_ataku: 3" in output
