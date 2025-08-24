from projekt.narzedzia import Singleton


class Flag(metaclass=Singleton):
    def __init__(self):
        if hasattr(self, "_initialized"):
            return
        self.track = False
        self.show = True
        self.klikniecie_flag = False
