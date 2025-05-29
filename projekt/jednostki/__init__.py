# init tworzy paczkę z folderu jednostki, pozwala na pisanie from projekt.jednostki import coś, bez tego trzeba by było pisac jeszcze projekt.import.dane.frakcja1 co jest karkołomne, dzielenie na paczki jest bardzo przydatne w dużym programie
from .klasy.wojownik import Wojownik
from .klasy.piechota import Piechota
from .dane.frakcja1 import *
