from projekt.assetMenager import AssetManager


class AkcjeMenager:
    def __init__(self, dane):
        self.akcje = []
        self.buffs = dane

    def applybuff(self, typ):
        self.akcje.append((AssetManager.get_akcje(typ, "tury"), typ, "turn"))
        self.akcje.append((AssetManager.get_akcje(typ, "cooldown"), typ, "cooldown"))

    def turn(self):
        for akcja in self.akcje:
            if akcja[0] - 1 == 0:
                self.reset_buff(akcja[1], akcja[2])
        self.akcje = [
            (akcja[0] - 1, akcja[1], akcja[2])
            for akcja in self.akcje
            if akcja[0] - 1 != 0
        ]
        print(self.akcje)

    def reset_buff(self, typ, rodzaj):
        if rodzaj == "cooldown":
            self.buffs[typ + "_cooldown"] = False
        else:
            self.buffs[typ] -= AssetManager.get_akcje(typ, "mnoznik")
