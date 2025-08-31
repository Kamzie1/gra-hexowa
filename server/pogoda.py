import random


class Pogoda:
    pogoda_init = [0, 0]
    propabilities = [0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 4]

    @classmethod
    def get_propability(cls, type):
        return cls.propabilities[type]

    @classmethod
    def update(cls, pogoda):
        pogoda[0] = pogoda[1]
        pogoda[1] = cls.get_propability(random.randint(0, 10))
        return pogoda
