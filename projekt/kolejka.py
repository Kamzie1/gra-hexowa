import pygame
from projekt.narzedzia import (
    Przycisk,
    PrzyciskReady,
    pozycja_myszy_na_surface,
    Display,
    Switch,
    ColorSwitch,
    IntInput,
    TeamSwitch,
    CheckBox,
)
from projekt.ustawienia import Width, Height, srodek
import random
from projekt.network import Client
from projekt.assetMenager import AssetManager


class Kolejka:
    def __init__(self):
        # atrybuty
        self.w = Width / 3
        self.h = Height / 1.5
        self.font = AssetManager.get_font("consolas", 20)

        # obiekty
        self.ready = PrzyciskReady(
            100, 34, "blue", (Width / 1.5, Height / 1.5), "Gotowy", "white"
        )
        self.leave = Przycisk(200, 34, (230, 230, 230), (5, 5), "Opuść kolejkę", "red")
        self.content = pygame.Surface((Width / 1.5, Height / 1.5))
        self.content_rect = self.content.get_frect(center=srodek)
        self.room_id = Display(400, 50, (srodek[0] - 200, 5), "consolas", 34)
        self.playerCard = PlayerCard()
        self.ustawienia = Ustawienia()

        # surface
        self.opponents = pygame.Surface((self.w - 30, self.h))
        self.opponents_rect = self.opponents.get_frect(topleft=(self.w / 2 + 30, 0))

    def run(self, screen):
        self.event_handler()
        self.draw(screen)

    def draw(self, screen):
        screen.fill("white")
        self.content.fill("white")

        self.displayPlayers()
        self.ustawienia.draw(self.content, Client().room)

        pygame.draw.line(
            self.content,
            "black",
            (self.w / 2, 0),
            (self.w / 2, self.h),
            width=1,
        )

        self.ready.draw(self.content)
        self.room_id.display(f"Id pokoju: {Client().room["room_id"]}", "black", screen)
        self.leave.draw(screen)

        screen.blit(self.content, self.content_rect)

    def displayPlayers(self):
        self.opponents.fill("white")
        x = 0
        y = 0
        for user in Client().room["users"]:
            if not user["name"] == Client().name:
                self.drawOpponentDisplay(x, y, user)
                x += 200
                if x > self.w / 2 + 155:
                    x = 0
                    y += 250
            else:
                self.playerCard.draw(Client().name, self.content)

        for user in Client().room["spectators"]:
            if not user["name"] == Client().name:
                self.drawOpponentDisplay(x, y, user)
                x += 200
                if x > self.w / 2 + 155:
                    x = 0
                    y += 250
            else:
                self.playerCard.draw(Client().name, self.content)

        self.content.blit(self.opponents, self.opponents_rect)

    def leave_event(self, mouse_pos):
        if self.leave.rect.collidepoint(mouse_pos):
            Client().ekran = 0
            try:
                Client().leave()
            except Exception as e:
                print(e)

    def event_handler(self):
        self.ustawienia.dirty = False
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = pozycja_myszy_na_surface(
            mouse_pos, (self.content_rect.x, self.content_rect.y)
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.ustawienia.event_handler(event, mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.ready.rect.collidepoint(mouse_pos):
                    self.ready.click()
                    Client().ustawienia(self.load_ustawienia())
                self.leave_event(pygame.mouse.get_pos())
                if self.playerCard.colorsButton.rect.collidepoint(mouse_pos):
                    self.playerCard.color += 1
                    self.playerCard.color %= len(self.playerCard.colors)
                    Client().ustawienia(self.load_ustawienia())

                if self.playerCard.fractionButton.rect.collidepoint(mouse_pos):
                    self.playerCard.fraction += 1
                    self.playerCard.fraction %= len(self.playerCard.frakcje)
                    Client().ustawienia(self.load_ustawienia())

                if self.playerCard.teamButton.rect.collidepoint(mouse_pos):
                    if Client().room["teams"]:
                        self.playerCard.team += 1
                        self.playerCard.team %= Client().room["teams"]
                        Client().ustawienia(self.load_ustawienia())
        if self.ustawienia.dirty:
            Client().ustawienia(self.load_ustawienia())

    def load_ustawienia(self):
        return {
            "ustawienia": {
                "map_id": self.ustawienia.map_id,
                "mapa": self.ustawienia.maps[self.ustawienia.map_id],
                "width": self.ustawienia.size[self.ustawienia.map_id][0],
                "height": self.ustawienia.size[self.ustawienia.map_id][1],
                "rivers": 2,
                "wioski": int(self.ustawienia.wioski.display),
                "gold": int(self.ustawienia.gold.display),
                "srebro": int(self.ustawienia.srebro.display),
                "stal": int(self.ustawienia.stal.display),
                "food": int(self.ustawienia.food.display),
                "medale": int(self.ustawienia.medale.display),
                "space-between": 10,
                "from-border": 5,
            },
            "ready": self.ready.value,
            "frakcja": self.playerCard.frakcje[self.playerCard.fraction],
            "color": self.playerCard.colors[self.playerCard.color],
            "team": self.playerCard.team,
            "ifPogoda": self.ustawienia.pogoda.value,
        }

    def drawOpponentDisplay(self, x, y, user):
        surf = pygame.Surface((150, 250))
        surf.fill((200, 200, 200))
        rect = surf.get_frect(topleft=(x, y))
        text = self.font.render(user["name"], True, "black")
        text_rect = text.get_frect(topleft=(20, 10))

        team = self.font.render(f"Team{user["team"]}", True, "black")
        team_rect = team.get_rect(bottomright=(140, 220))

        fraction = self.font.render(user["frakcja"], True, "black")
        fraction_rect = fraction.get_rect(bottomright=(140, 250))

        surf.blit(text, text_rect)
        surf.blit(fraction, fraction_rect)
        surf.blit(team, team_rect)
        self.opponents.blit(surf, rect)
        if user["color"] is not None:
            pygame.draw.rect(self.opponents, user["color"], rect, width=3)


class PlayerCard:
    def __init__(self):
        self.surf = pygame.Surface((250, 500))
        self.surf.fill((200, 200, 200))
        self.rect = self.surf.get_frect(topleft=(0, 0))
        self.font = AssetManager.get_font("consolas", 20)

        self.frakcje = ["Japonia", "Prusy", "Spectator"]
        self.colors = ["red", "blue"]

        self.fraction = 0
        self.color = 0
        self.team = 0
        self.buttonGroup = pygame.sprite.Group()

        self.teamButton = TeamSwitch(250, 50, (250, 440))
        self.fractionButton = Switch(250, 50, (250, 500), self.frakcje)
        self.colorsButton = ColorSwitch(50, 50, (260, 0), self.colors)

    def draw(self, name, screen):
        self.surf.fill((200, 200, 200))
        self.fractionButton.draw(self.fraction, self.surf)
        self.colorsButton.draw(self.color, screen)
        self.teamButton.draw(self.team, self.surf)

        # imie
        text = self.font.render(name, True, "black")
        text_rect = text.get_frect(topleft=(20, 10))
        self.surf.blit(text, text_rect)

        screen.blit(self.surf, self.rect)

        if self.color is not None:
            pygame.draw.rect(screen, self.colors[self.color], self.rect, width=3)


class Ustawienia:
    def __init__(self):
        self.surf = pygame.Surface((Width / 7, Height / 2))
        self.rect = self.surf.get_frect(topright=(Width / 1.5, 0))
        self.wioskiLabel = Display(Width / 8, 20, (0, 0), "consolas", 16)
        self.wioski = IntInput(Width / 8, 20, (0, 30), "grey", "black", "15", 16)
        self.goldLabel = Display(Width / 8, 20, (0, 60), "consolas", 16)
        self.gold = IntInput(Width / 8, 20, (0, 90), "grey", "black", "1000", 16)
        self.srebroLabel = Display(Width / 8, 20, (0, 120), "consolas", 16)
        self.srebro = IntInput(Width / 8, 20, (0, 150), "grey", "black", "1000", 16)
        self.stalLabel = Display(Width / 8, 20, (0, 180), "consolas", 16)
        self.stal = IntInput(Width / 8, 20, (0, 210), "grey", "black", "1000", 16)
        self.foodLabel = Display(Width / 8, 20, (0, 240), "consolas", 16)
        self.food = IntInput(Width / 8, 20, (0, 270), "grey", "black", "1000", 16)
        self.medaleLabel = Display(Width / 8, 20, (0, 300), "consolas", 16)
        self.medale = IntInput(Width / 8, 20, (0, 330), "grey", "black", "1000", 16)
        self.pogodaLabel = Display(Width / 16, 30, (0, 390), "consolas", 20)
        self.pogoda = CheckBox(20, 20, (Width / 16, 405))
        self.maps = ["mapa1(30x30)", "mapa2(10x10)", "mapa3(40x40)", "random"]
        self.size = [(30, 30), (10, 10), (40, 40), (0, 0)]
        self.map_id = 0
        self.mapaSwitch = Switch(Width / 8, 50, (Width / 8, 500), self.maps)

    def draw(self, screen, room):
        self.map_id = room["ustawienia"]["map_id"]
        self.wioski.display = str(room["ustawienia"]["wioski"])
        self.gold.display = str(room["ustawienia"]["gold"])
        self.srebro.display = str(room["ustawienia"]["srebro"])
        self.stal.display = str(room["ustawienia"]["stal"])
        self.food.display = str(room["ustawienia"]["food"])
        self.medale.display = str(room["ustawienia"]["medale"])
        self.pogoda.value = room["ifPogoda"]
        self.surf.fill("white")
        self.wioskiLabel.display("Wioski:", "black", self.surf)
        self.wioski.draw(self.surf)
        self.goldLabel.display("Złoto:", "black", self.surf)
        self.gold.draw(self.surf)
        self.srebroLabel.display("Srebro:", "black", self.surf)
        self.srebro.draw(self.surf)
        self.stalLabel.display("Stal:", "black", self.surf)
        self.stal.draw(self.surf)
        self.foodLabel.display("Jedzenie:", "black", self.surf)
        self.food.draw(self.surf)
        self.medaleLabel.display("Medale:", "black", self.surf)
        self.medale.draw(self.surf)
        self.pogodaLabel.display("Pogoda:", "black", self.surf)
        self.pogoda.display(self.surf)
        self.mapaSwitch.draw(self.map_id, self.surf)
        screen.blit(self.surf, self.rect)

    def event_handler(self, event, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
            self.wioski.update(event, mouse_pos)
            self.gold.update(event, mouse_pos)
            self.srebro.update(event, mouse_pos)
            self.stal.update(event, mouse_pos)
            self.food.update(event, mouse_pos)
            self.medale.update(event, mouse_pos)
            self.pogoda.event(event, mouse_pos)
            if (
                event.type == pygame.MOUSEBUTTONUP
                and event.button == 1
                and self.mapaSwitch.rect.collidepoint(mouse_pos)
            ):
                self.map_id += 1
                self.map_id %= len(self.maps)
                self.dirty = True
            if self.wioski.dirty:
                self.dirty = True
            if (
                self.gold.dirty
                or self.srebro.dirty
                or self.stal.dirty
                or self.food.dirty
                or self.medale.dirty
                or self.pogoda.dirty
            ):
                self.dirty = True
