from .klasy.wojownik import Wojownik
from .klasy.squad import Squad
from .klasy.miasto import Miasto
from .dane.Japonia import Japonia


def get_fraction(frakcja):
    match (frakcja):
        case "japonia":
            return Japonia
        case _:
            raise ValueError
