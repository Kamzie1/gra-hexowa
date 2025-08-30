import pygame
from projekt.assetMenager import AssetManager
from .buttons import SquadButtonDisplay, TextButton
from projekt.network import Client
from projekt.narzedzia import pozycja_myszy_na_surface, get_sasiedzi, MouseDisplay
from .mapa import Mapa
from projekt.jednostki import Squad, Budynek


class InzynierBuild:
    def __init__(self, Width, Height, pos):
        self.show = False
        self.surf = pygame.Surface((Width, Height))
        self.surf.fill("white")
        self.rect = self.surf.get_frect(center=pos)
        self.building_group = pygame.sprite.Group()
        self.setup()

    def setup(self):
        SquadBlock(
            self.building_group,
            350,
            200,
            (20, 20),
            Client().player.frakcja["specjalne"][1],
            Client().player.color,
        )
        BuildingBlock(
            self.building_group,
            350,
            200,
            (20, 270),
            Client().player.frakcja["budynek"][5],
            Client().player.color,
        )

    def draw(self, screen):
        self.surf.fill("white")
        for budynek in self.building_group:
            budynek.draw(self.surf)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos, x, y):
        if self.show and self.rect.collidepoint(mouse_pos):
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
            for budynek in self.building_group:
                budynek.event(mouse_pos, x, y)
                if budynek.dirty:
                    self.show = False


class Block(pygame.sprite.Sprite):
    def __init__(self, group, Width, Height, pos, budynek, color):
        super().__init__(group)
        self.pos = pos
        self.surf = pygame.Surface((Width, Height))
        self.surf.fill("white")
        self.rect = self.surf.get_frect(topleft=pos)
        self.font = AssetManager.get_font("consolas", 16)
        self.title_font = AssetManager.get_font("consolas", 20)
        self.budynek = budynek
        self.color = color
        self.width = Width
        self.height = Height
        self.dirty = False
        self.button_group = pygame.sprite.Group()
        self.buy = TextButton(
            50,
            30,
            "red",
            (250, self.height / 2),
            self.button_group,
            "Kup",
            "consolas",
            20,
            "white",
        )

    def event(self, mouse_pos, x, y):
        if self.rect.collidepoint(mouse_pos):
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
            if self.buy.rect.collidepoint(mouse_pos):
                self.dirty = True
                Mapa().move_flag = self.load()
                self.get_positions(x, y)

    def load(self):
        return None

    def get_positions(self, x, y):
        sasiadx, sasiady = get_sasiedzi(x, y)
        Mapa().correct_moves[x][y] = -1
        for i in range(6):
            if x + sasiadx[i] < 0 or x + sasiadx[i] >= Mapa().width:
                continue
            if y + sasiady[i] < 0 or y + sasiady[i] >= Mapa().height:
                continue
            if Mapa().Tile_array[x + sasiadx[i]][y + sasiady[i]].jednostka is not None:
                continue
            Mapa().correct_moves[x + sasiadx[i]][y + sasiady[i]] = 0
            Mapa().move_group.empty()

    def draw(self, screen):
        self.surf.fill("white")
        title = self.title_font.render(self.budynek["nazwa"], True, "black")
        self.surf.blit(title, title.get_frect(center=(self.width / 2, 15)))
        image = AssetManager.get_unit(self.budynek["nazwa"], self.color)
        self.surf.blit(image, image.get_frect(center=(60, self.height / 2)))
        self.display_cost()
        self.surf.blit(self.buy.image, self.buy.rect)
        screen.blit(self.surf, self.rect)

    def display_cost(self):
        y = 0
        types = ["srebro", "stal", "zloto", "food", "medale"]
        cost = self.budynek["cost"]
        for currency in types:
            if cost[currency]:
                self.display_currency(y, currency, cost[currency])
                y += 1

    def display_currency(self, y, currency, cost):
        image = AssetManager.get_asset(currency)
        scaled_image = pygame.transform.scale(image, (25, 25))
        self.surf.blit(
            scaled_image,
            scaled_image.get_frect(topleft=(150, 40 + 40 * y)),
        )
        text = self.font.render(str(cost), True, "black")
        self.surf.blit(text, text.get_frect(topleft=(200, 40 + 40 * y)))


class BuildingBlock(Block):
    def __init__(self, group, Width, Height, pos, budynek, color):
        super().__init__(group, Width, Height, pos, budynek, color)

    def load(self):
        info = {}
        info["color"] = Client().player.color
        info["owner"] = Client().player.name
        info["owner_id"] = Client().player.id
        info["pos"] = (5000, 5000)
        info["id"] = self.budynek["id"]
        info["team"] = Client().player.team
        return Budynek(Mapa().building_group, info, None, Client().player.frakcja)

    def draw(self, screen):
        self.surf.fill("white")
        title = self.title_font.render(self.budynek["nazwa"], True, "black")
        self.surf.blit(title, title.get_frect(center=(self.width / 2, 15)))
        image = AssetManager.get_asset(self.budynek["nazwa"])
        self.surf.blit(image, image.get_frect(center=(60, self.height / 2)))
        self.display_cost()
        self.surf.blit(self.buy.image, self.buy.rect)
        screen.blit(self.surf, self.rect)

    def get_positions(self, x, y):
        sasiadx, sasiady = get_sasiedzi(x, y)
        Mapa().correct_moves = [
            [-1 for _ in range(Mapa().width)] for _ in range(Mapa().height)
        ]
        Mapa().correct_moves[x][y] = -1
        for i in range(6):
            if x + sasiadx[i] < 0 or x + sasiadx[i] >= Mapa().width:
                continue
            if y + sasiady[i] < 0 or y + sasiady[i] >= Mapa().height:
                continue
            if (
                Mapa().Tile_array[x + sasiadx[i]][y + sasiady[i]].budynek is not None
                and Mapa().Tile_array[x + sasiadx[i]][y + sasiady[i]].budynek.id < 5
            ):
                continue
            Mapa().correct_moves[x + sasiadx[i]][y + sasiady[i]] = 0
            Mapa().move_group.empty()


class SquadBlock(Block):
    def __init__(self, group, Width, Height, pos, budynek, color):
        super().__init__(group, Width, Height, pos, budynek, color)

    def load(self):
        info = {}
        info["color"] = Client().player.color
        info["owner"] = Client().player.name
        info["owner_id"] = Client().player.id
        info["pos"] = (5000, 5000)
        info["strategy"] = 0
        info["wzmocnienie"] = 0
        info["team"] = Client().player.team
        info["jednostki"] = []
        jednostka = self.budynek
        jednostka["array_pos"] = 3
        info["jednostki"].append(jednostka)
        return Squad(Mapa().army_group, info, None, Client().player.frakcja)


class InzynierButton(SquadButtonDisplay):
    def __init__(self, width, height, color, pos, tekst=None):
        super().__init__(width, height, color, pos, tekst)

    def event(self, mouse_pos, move_flag, inzynierBuild):
        if move_flag is None:
            return
        if move_flag.inzynier() and self.rect.collidepoint(mouse_pos):
            self.click(inzynierBuild)

    def click(self, inzynierBuild):
        inzynierBuild.show = not inzynierBuild.show

    def hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            MouseDisplay().update(mouse_pos, "Lista budynków do budowy")

    def draw(self, screen):
        screen.blit(self.image, self.rect)
