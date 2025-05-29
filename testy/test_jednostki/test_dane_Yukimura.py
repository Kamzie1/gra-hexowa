from projekt.jednostki import Yukimura_Sanada as y
from projekt.jednostki import Piechota


def test_inicjalizacja():
    Yukimura_Sanada = Piechota(
        y["zdrowie"],
        y["morale"],
        y["ruch"],
        y["przebicie"],
        y["pancerz"],
        y["atak"],
        y["koszt_ataku"],
    )

    assert Yukimura_Sanada.zdrowie == y["zdrowie"]
    assert Yukimura_Sanada.morale == y["morale"]
    assert Yukimura_Sanada.ruch == y["ruch"]
    assert Yukimura_Sanada.przebicie == y["przebicie"]
    assert Yukimura_Sanada.pancerz == y["pancerz"]
    assert Yukimura_Sanada.atak == y["atak"]
    assert Yukimura_Sanada.koszt_ataku == y["koszt_ataku"]
