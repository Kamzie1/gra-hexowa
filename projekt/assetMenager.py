import pygame
from os.path import join
import yaml


class AssetManager:
    assets = ["turn", "złoto", "menu", "armor"]
    maps = {}
    mapy = ["mapa1(30x30)"]
    efekty_heksow = [
        "blue_podswietlenie",
        "red_podswietlenie",
        "grey_podswietlenie",
        "hex-klikniecie",
        "hex-klikniecie (2)",
        "hex-klikniecie (3)",
        "white_podswietlenie",
    ]
    font_assets = ["consolas"]
    fonts = {}
    images = {}
    tiles = {}

    @staticmethod
    def preload_assets():
        AssetManager.load_fractions()
        AssetManager.load_common_assets()
        AssetManager.load_heks_effects()
        AssetManager.load_fonts()
        AssetManager.load_hex()
        AssetManager.load_mapy()
        for frakcja in AssetManager.frakcja:
            AssetManager.load_fraction(frakcja)
        AssetManager.load_akcje()

    @staticmethod
    def load_common_assets():
        for asset in AssetManager.assets:
            path = asset + ".png"
            AssetManager.images[asset] = pygame.image.load(
                join("Grafika", path)
            ).convert_alpha()

    @staticmethod
    def load_heks_effects():
        for image in AssetManager.efekty_heksow:
            path = image + ".png"
            AssetManager.images[image] = pygame.image.load(
                join("Grafika", "tile-grafika", "efekty hexów", path)
            )

    @staticmethod
    def load_fonts():
        for font in AssetManager.font_assets:
            path = font + ".ttf"
            AssetManager.fonts[font] = {
                10: pygame.font.Font(join("Grafika", "fonts", path), 10),
                16: pygame.font.Font(join("Grafika", "fonts", path), 16),
                20: pygame.font.Font(join("Grafika", "fonts", path), 20),
                24: pygame.font.Font(join("Grafika", "fonts", path), 24),
                26: pygame.font.Font(join("Grafika", "fonts", path), 26),
                100: pygame.font.Font(join("Grafika", "fonts", path), 100),
            }

    @staticmethod
    def load_fractions():
        with open(
            join("projekt", "dane", "jednostki", "inne.yaml"), "r", encoding="utf-8"
        ) as f:
            AssetManager.inne = yaml.safe_load(f)
        with open(
            join("projekt", "dane", "jednostki", "bronie.yaml"), "r", encoding="utf-8"
        ) as f:
            AssetManager.bronie = yaml.safe_load(f)
        with open(
            join("projekt", "dane", "jednostki", "Japonia.yaml"), "r", encoding="utf-8"
        ) as f:
            AssetManager.frakcja = yaml.safe_load(f)

        for frakcja in AssetManager.frakcja:
            for unit in AssetManager.frakcja[frakcja]["jednostka"]:
                resolved_bronie = [
                    AssetManager.bronie[nazwa] for nazwa in unit["bronie"]
                ]
                unit["wzrok"] = AssetManager.inne[unit["wzrok"]]
                unit["bronie"] = resolved_bronie

            for unit in AssetManager.frakcja[frakcja]["specjalne"]:
                resolved_bronie = [
                    AssetManager.bronie[nazwa] for nazwa in unit["bronie"]
                ]
                unit["wzrok"] = AssetManager.inne[unit["wzrok"]]
                unit["bronie"] = resolved_bronie

    @staticmethod
    def load_fraction(fraction):
        for wojownik in AssetManager.frakcja[fraction]["jednostka"]:
            AssetManager.images[wojownik["nazwa"]] = {}
            AssetManager.images[wojownik["nazwa"]]["red"] = pygame.image.load(
                join("Grafika", "jednostki-grafika", wojownik["red"])
            ).convert_alpha()
            AssetManager.images[wojownik["nazwa"]]["blue"] = pygame.image.load(
                join("Grafika", "jednostki-grafika", wojownik["blue"])
            ).convert_alpha()

        for budynek in AssetManager.frakcja[fraction]["budynek"]:
            AssetManager.images[budynek["nazwa"]] = pygame.image.load(
                join("Grafika", "budynki-grafika", budynek["image"])
            ).convert_alpha()

        for wojownik in AssetManager.frakcja[fraction]["specjalne"]:
            AssetManager.images[wojownik["nazwa"]] = {}
            AssetManager.images[wojownik["nazwa"]]["red"] = pygame.image.load(
                join("Grafika", "jednostki-grafika", wojownik["red"])
            ).convert_alpha()
            AssetManager.images[wojownik["nazwa"]]["blue"] = pygame.image.load(
                join("Grafika", "jednostki-grafika", wojownik["blue"])
            ).convert_alpha()

    @staticmethod
    def load_hex():
        with open(join("projekt", "dane", "dane_hex.yaml"), "r", encoding="utf-8") as f:
            AssetManager.tiles = yaml.safe_load(f)

        for tile in AssetManager.tiles["tileproperties"]:
            tile["image"] = pygame.image.load(
                join("Grafika", "tile-grafika", "hexy", tile["image"] + ".png")
            ).convert_alpha()

    @staticmethod
    def load_akcje():
        with open(
            join("projekt", "dane", "dane_akcje.yaml"), "r", encoding="utf-8"
        ) as f:
            AssetManager.akcje = yaml.safe_load(f)

    @staticmethod
    def load_mapy():
        for mapa in AssetManager.mapy:
            with open(
                join("projekt", "dane", "mapy", mapa + ".yaml"), "r", encoding="utf-8"
            ) as f:
                AssetManager.maps[mapa] = yaml.safe_load(f)

    @staticmethod
    def get_asset(name):
        return AssetManager.images[name]

    @staticmethod
    def get_unit(name, color):
        return AssetManager.images[name][color]

    @staticmethod
    def get_font(name, size):
        return AssetManager.fonts[name][size]

    @staticmethod
    def get_koszt(name, level=None):
        if level is None:
            return AssetManager.akcje[name]["koszt"]
        return AssetManager.akcje[name][level - 1]["koszt"]

    @staticmethod
    def get_mnoznik(name, level=None):
        if level is None:
            return AssetManager.akcje[name]["mnoznik"]
        return AssetManager.akcje[name][level - 1]["mnoznik"]

    @staticmethod
    def get_akcje(name, other=None):
        if other is None:
            return AssetManager.akcje[name]
        return AssetManager.akcje[name][other]

    @staticmethod
    def get_tiles_property(id):
        return AssetManager.tiles["tileproperties"][id]
