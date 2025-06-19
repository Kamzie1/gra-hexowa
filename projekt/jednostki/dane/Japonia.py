# Dane frakcji nr. 1


# dane jednostki Yukimura Sanda w schemacie słownika, dostęp do danych: Yukimura_Sanda['nazwa_informacji'] np. Yukimura_Sanda['zdrowie'] da nam 500
Yukimura_Sanada = {
    "nazwa": "Yukimura Sanada",
    "zdrowie": 500,
    "morale": 100,
    "ruch": 15,
    "przebicie": 10,
    "pancerz": 8,
    "atak": 20,
    "koszt_ataku": 3,
    "red": "Yukimura_Sanada_red.png",
    "blue": "Yukimura_Sanada_blue.png",
    "cost": 500,
    "id": 1,
}

Bodyguard = {
    "nazwa": "Bodyguard",
    "zdrowie": 100,
    "morale": 70,
    "ruch": 10,
    "przebicie": 6,
    "pancerz": 4,
    "atak": 10,
    "koszt_ataku": 3,
    "red": "Bodyguard_red.png",
    "blue": "Bodyguard_blue.png",
    "cost": 100,
    "id": 0,
}

Kolumbryna = {
    "nazwa": "Kolumbryna",
    "zdrowie": 80,
    "morale": 90,
    "ruch": 5,
    "przebicie": 12,
    "pancerz": 2,
    "atak": 20,
    "koszt_ataku": 4,
    "red": "kolubryna.png",
    "blue": "kolubryna.png",
    "id": 2,
    "cost": 400,
}

Miasto = {
    "nazwa": "Miasto",
    "zdrowie": 20,
    "morale": 90,
    "przebicie": 15,
    "pancerz": 20,
    "atak": 30,
    "koszt_ataku": 2,
    "red": "recruit_test.png",
    "blue": "recruit_test.png",
    "earn": {
        "gold": 400,
    },
    "heal": 40,
}

Japonia = {
    "jednostka": [
        Bodyguard,
        Yukimura_Sanada,
        Kolumbryna,
    ],
    "miasto": Miasto,
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
