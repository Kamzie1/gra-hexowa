from .klasy.wojownik import Wojownik
from .klasy.squad import Squad
from .klasy.miasto import Miasto
from .klasy.wioska import Wioska
from .dane.Japonia import Japonia, Japonia2


def get_fraction(frakcja):
    match (frakcja):
        case "Japonia":
            return Japonia
        case "Japonia2":
            return Japonia2
        case _:
            raise ValueError
