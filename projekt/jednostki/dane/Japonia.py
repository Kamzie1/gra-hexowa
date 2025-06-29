from .bronie import *
from .inne import *

# Dane frakcji nr. 1


# dane jednostek w schemacie słownika, dostęp do danych: Frakcja['typ jednostki']['id']['informacja'] np. Japonia['jednostki'][0]['zdrowie'] da nam 70

Japonia = {
    "jednostka": [
        {
            "nazwa": "Bodyguard",
            "zdrowie": 70,
            "morale": 70,
            "ruch": 12,
            "bronie": [Katana],
            "wzrok": Oczy,
            "pancerz": 4,
            "atak_points": 9,
            "red": "Bodyguard_red.png",
            "blue": "Bodyguard_blue.png",
            "cost": 120,
            "id": 0,
            "kategoria": "jednostka",
        },
        {
            "nazwa": "Włócznik",
            "zdrowie": 60,
            "morale": 90,
            "ruch": 10,
            "bronie": [Wlocznia],
            "wzrok": Oczy,
            "pancerz": 3,
            "atak_points": 9,
            "red": "włócznik.png",
            "blue": "włócznik.png",
            "id": 1,
            "cost": 200,
            "kategoria": "jednostka",
        },
        {
            "nazwa": "Yukimura Sanada",
            "zdrowie": 100,
            "morale": 100,
            "ruch": 15,
            "bronie": [Yumonji_Jari_2],
            "wzrok": Oczy,
            "pancerz": 8,
            "atak_points": 12,
            "red": "Yukimura_Sanada_red.png",
            "blue": "Yukimura_Sanada_blue.png",
            "cost": 400,
            "id": 2,
            "kategoria": "jednostka",
        },
        {
            "nazwa": "Kolumbryna",
            "zdrowie": 55,
            "morale": 90,
            "ruch": 8,
            "bronie": [Kolumbryna],
            "wzrok": Lornetka,
            "pancerz": 2,
            "atak_points": 8,
            "red": "kolubryna.png",
            "blue": "kolubryna.png",
            "id": 3,
            "cost": 300,
            "kategoria": "jednostka",
        },
    ],
    "specjalne": [
        {
            "nazwa": "Miasto",
            "zdrowie": 500,
            "morale": 90,
            "ruch": 0,
            "bronie": [Kolumbryna],
            "wzrok": Lornetka,
            "pancerz": 10,
            "atak_points": 16,
            "red": "rec2.png",
            "blue": "rec2.png",
            "id": 0,
            "kategoria": "specjalne",
        }
    ],
    "budynek": [
        {
            "nazwa": "Miasto",
            "red": "miasto.png",
            "blue": "miasto.png",
            "earn": {
                "gold": 30,
            },
            "heal": 10,
            "id": 0,
            "kategoria": "budynek",
        },
        {
            "nazwa": "Wioska",
            "red": "miasto.png",
            "blue": "miasto.png",
            "grey": "miasto.png",
            "earn": {
                "gold": 30,
            },
            "heal": 10,
            "id": 1,
            "kategoria": "budynek",
        },
    ],
}
