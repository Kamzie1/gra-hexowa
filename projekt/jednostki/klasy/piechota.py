from .wojownik import Wojownik


# klasa piechota, dzieczy od klasy wojownik, implementuje specjalne działania piechoty
class Piechota(Wojownik):

    def __init__(self, zdrowie, morale, ruch, przebicie, pancerz, atak, koszt_ataku):
        # dziedziczenie od klasy Wojownik oznaczane jest słowem super()
        super().__init__(
            zdrowie=zdrowie,
            morale=morale,
            ruch=ruch,
            przebicie=przebicie,
            pancerz=pancerz,
            atak=atak,
            koszt_ataku=koszt_ataku,
        )
