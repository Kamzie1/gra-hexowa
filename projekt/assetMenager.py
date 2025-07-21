import pygame
from os.path import join
import yaml


class AssetManager:
    assets = ["turn", "złoto", "menu", "armor"]
    map_assets = ["tile-set.png"]
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

    @staticmethod
    def preload_assets():
        AssetManager.load_fractions()
        AssetManager.load_common_assets()
        AssetManager.load_heks_effects()
        AssetManager.load_fonts()
        for frakcja in AssetManager.frakcja:
            AssetManager.load_fraction(frakcja)

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
    def get_asset(name):
        return AssetManager.images[name]

    @staticmethod
    def get_unit(name, color):
        return AssetManager.images[name][color]

    @staticmethod
    def get_font(name, size):
        return AssetManager.fonts[name][size]
