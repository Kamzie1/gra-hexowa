import pygame
from projekt.narzedzia import (
    Przycisk,
    PrzyciskReady,
    pozycja_myszy_na_surface,
    Display,
    Switch,
    ColorSwitch,
)
from projekt.ustawienia import Width, Height, srodek


class Kolejka:
    def __init__(self):
        # atrybuty
        self.w = Width / 3
        self.h = Height / 1.5
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", 20)

        # obiekty
        self.ready = PrzyciskReady(
            100, 34, "blue", (Width / 1.5, Height / 1.5), "Gotowy", "white"
        )
        self.leave = Przycisk(200, 34, (230, 230, 230), (5, 5), "Opuść kolejkę", "red")
        self.content = pygame.Surface((Width / 1.5, Height / 1.5))
        self.content_rect = self.content.get_frect(center=srodek)
        self.room_id = Display(400, 50, (srodek[0] - 200, 5), "consolas.ttf", 34)
        self.playerCard = PlayerCard()

        # surface
        self.opponents = pygame.Surface((self.w + self.w / 3, self.h))
        self.opponents_rect = self.opponents.get_frect(topleft=(self.w / 3 * 2, 0))

    def run(self, screen, client):
        self.event_handler(client)
        self.draw(screen, client)

    def draw(self, screen, client):
        screen.fill("white")
        self.content.fill("white")

        self.displayPlayers(client)

        pygame.draw.line(
            self.content,
            "black",
            (self.w / 2, 0),
            (self.w / 2, self.h),
            width=1,
        )

        self.ready.draw(self.content)
        self.room_id.display(f"Id pokoju: {client.room["room_id"]}", "black", screen)
        self.leave.draw(screen)

        screen.blit(self.content, self.content_rect)

    def displayPlayers(self, client):
        self.opponents.fill("white")
        x = 0
        y = 0
        for user in client.room["users"]:
            if not user["name"] == client.name:
                self.drawOpponentDisplay(x, y, user)
                x += 250
                if x > self.w:
                    x = 0
                    y += 350
            else:
                self.playerCard.draw(client.name, self.content)
        self.content.blit(self.opponents, self.opponents_rect)

    def leave_event(self, client, mouse_pos):
        if self.leave.rect.collidepoint(mouse_pos):
            client.ekran = 0
            try:
                client.leave()
            except Exception as e:
                print(e)

    def event_handler(self, client):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.ready.rect.collidepoint(
                    pozycja_myszy_na_surface(
                        mouse_pos, (self.content_rect.x, self.content_rect.y)
                    )
                ):
                    print("click")
                    self.ready.click()
                    client.ustawienia(self.load_ustawienia())
                self.leave_event(client, mouse_pos)
                mouse_pos = pozycja_myszy_na_surface(
                    mouse_pos, (self.content_rect.x, self.content_rect.y)
                )
                if self.playerCard.colorsButton.rect.collidepoint(mouse_pos):
                    self.playerCard.color += 1
                    self.playerCard.color %= len(self.playerCard.colors)
                    client.ustawienia(self.load_ustawienia())

                if self.playerCard.fractionButton.rect.collidepoint(mouse_pos):
                    self.playerCard.fraction += 1
                    self.playerCard.fraction %= len(self.playerCard.frakcje)
                    client.ustawienia(self.load_ustawienia())

    def load_ustawienia(self):
        return {
            "ustawienia": {
                "mapa": "mapa_test1",
                "width": 30,
                "height": 30,
                "rivers": 2,
                "wioski": 15,
                "space-between": 10,
                "from-border": 5,
            },
            "ready": self.ready.value,
            "fraction": self.playerCard.frakcje[self.playerCard.fraction],
            "color": self.playerCard.colors[self.playerCard.color],
        }

    def drawOpponentDisplay(self, x, y, user):
        surf = pygame.Surface((150, 250))
        surf.fill((200, 200, 200))
        rect = surf.get_frect(topleft=(x, y))
        text = self.font.render(user["name"], True, "black")
        text_rect = text.get_frect(topleft=(20, 10))

        fraction = self.font.render(user["fraction"], True, "black")
        fraction_rect = fraction.get_rect(bottomright=(150, 250))

        surf.blit(text, text_rect)
        surf.blit(fraction, fraction_rect)
        self.opponents.blit(surf, rect)
        if user["color"] is not None:
            pygame.draw.rect(self.opponents, user["color"], rect, width=3)


class PlayerCard:
    def __init__(self):
        self.surf = pygame.Surface((250, 500))
        self.surf.fill((200, 200, 200))
        self.rect = self.surf.get_frect(topleft=(0, 0))
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", 20)
        self.frakcje = ["Japonia", "Japonia2"]
        self.colors = ["red", "blue"]

        self.fraction = 0
        self.color = 0
        self.buttonGroup = pygame.sprite.Group()

        self.fractionButton = Switch(250, 100, (250, 500), self.frakcje)
        self.colorsButton = ColorSwitch(50, 50, (260, 0), self.colors)

    def draw(self, name, screen):

        self.fractionButton.draw(self.fraction, self.surf)
        self.colorsButton.draw(self.color, screen)

        # imie
        text = self.font.render(name, True, "black")
        text_rect = text.get_frect(topleft=(20, 10))
        self.surf.blit(text, text_rect)

        screen.blit(self.surf, self.rect)

        if self.color is not None:
            pygame.draw.rect(screen, self.colors[self.color], self.rect, width=3)
