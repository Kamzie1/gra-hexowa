# Dane frakcji nr. 1


# dane jednostki Yukimura Sanda w schemacie słownika, dostęp do danych: Yukimura_Sanda['nazwa_informacji'] np. Yukimura_Sanda['zdrowie'] da nam 500
Yukimura_Sanada = {
    "nazwa": "Yukimura Sanada",
    "zdrowie": 100,
    "morale": 100,
    "ruch": 15,
    "przebicie": 10,
    "pancerz": 8,
    "atak": 20,
    "koszt_ataku": 3,
    "atak_points": 12,
    "range": 1,
    "red": "Yukimura_Sanada_red.png",
    "blue": "Yukimura_Sanada_blue.png",
    "cost": 500,
    "id": 1,
    "kategoria": "jednostka",
}

Bodyguard = {
    "nazwa": "Bodyguard",
    "zdrowie": 60,
    "morale": 70,
    "ruch": 10,
    "przebicie": 6,
    "pancerz": 4,
    "atak": 10,
    "koszt_ataku": 3,
    "atak_points": 9,
    "range": 1,
    "red": "Bodyguard_red.png",
    "blue": "Bodyguard_blue.png",
    "cost": 100,
    "id": 0,
    "kategoria": "jednostka",
}

Kolumbryna = {
    "nazwa": "Kolumbryna",
    "zdrowie": 55,
    "morale": 90,
    "ruch": 5,
    "przebicie": 12,
    "pancerz": 2,
    "atak": 20,
    "koszt_ataku": 4,
    "atak_points": 8,
    "range": 3,
    "red": "kolubryna.png",
    "blue": "kolubryna.png",
    "id": 2,
    "cost": 400,
    "kategoria": "jednostka",
}

Miastow = {
    "nazwa": "Miasto",
    "zdrowie": 500,
    "morale": 90,
    "ruch": 0,
    "przebicie": 15,
    "pancerz": 10,
    "atak": 30,
    "koszt_ataku": 4,
    "atak_points": 12,
    "range": 2,
    "red": "rec2.png",
    "blue": "rec2.png",
    "id": 0,
    "kategoria": "specjalne",
}

Miasto = {
    "nazwa": "Miasto",
    "red": "miasto.png",
    "blue": "miasto.png",
    "earn": {
        "gold": 400,
    },
    "heal": 10,
    "id": 0,
    "kategoria": "budynek",
}

Japonia = {
    "jednostka": [
        Bodyguard,
        Yukimura_Sanada,
        Kolumbryna,
    ],
    "specjalne": [Miastow],
    "budynek": [Miasto],
}

Japonia2 = [
    Bodyguard,
    Yukimura_Sanada,
    Kolumbryna,
    Bodyguard,
    Yukimura_Sanada,
    Kolumbryna,
]


def get_fraction(frakcja):
    match (frakcja):
        case "japonia":
            return Japonia
        case "japonia2":
            return Japonia2
        case _:
            raise ValueError
