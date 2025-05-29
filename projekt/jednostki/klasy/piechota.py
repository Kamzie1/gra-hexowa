from .wojownik import Wojownik


class Piechota(Wojownik):

    def __init__(self, zdrowie, morale, ruch, przebicie, pancerz, atak, koszt_ataku):
        super().__init__(
            zdrowie=zdrowie,
            morale=morale,
            ruch=ruch,
            przebicie=przebicie,
            pancerz=pancerz,
            atak=atak,
            koszt_ataku=koszt_ataku,
        )
