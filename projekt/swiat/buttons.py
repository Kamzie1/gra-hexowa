from projekt.jednostki import Squad
import pygame
from os.path import join
from projekt.assetMenager import AssetManager
from .squadDisplay import SquadDisplay
from .mapa import Mapa
from projekt.network import Client
from projekt.akcjeMenager import AkcjeMenager
from projekt.flag import Flag
import random


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        button_group,
        description,
        image_name=None,
    ) -> None:
        super().__init__(button_group)
        if image_name is None:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            self.image = AssetManager.get_asset(image_name)
        self.pos = pos
        self.rect = self.image.get_frect(topleft=self.pos)
        self.description = description
        self.color = color

    def click(self, *args):
        pass

    def hover(self):
        pass

    def draw(self):
        self.image.fill(self.color)

    def display_cost(self, cost, screen, count=0):
        y = 0
        types = ["srebro", "stal", "zloto", "food", "medale"]
        for currency in types:
            if cost[currency]:
                if count == 0:
                    self.display_currency(y, currency, cost[currency], screen)
                elif count > 0:
                    self.display_currency(y, currency, cost[currency] * count, screen)
                y += 1

    def display_currency(self, y, currency, cost, screen):
        image = AssetManager.get_asset(currency)
        scaled_image = pygame.transform.scale(image, (25, 25))
        screen.blit(
            scaled_image,
            scaled_image.get_frect(
                topleft=(self.pos[0] + 65, self.pos[1] + 5 + 25 * y)
            ),
        )
        text = AssetManager.get_font("consolas", 16).render(str(cost), True, "white")
        screen.blit(
            text, text.get_frect(topleft=(self.pos[0] + 85, self.pos[1] + 8 + 25 * y))
        )


class TextButton(pygame.sprite.Sprite):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        button_group,
        tekst,
        font="consolas",
        font_size=24,
        font_color="black",
    ) -> None:
        super().__init__(button_group)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.font = AssetManager.get_font(font, font_size)
        text_surf = self.font.render(tekst, True, font_color)
        text_rect = text_surf.get_rect(center=(width / 2, height / 2))
        self.image.blit(text_surf, text_rect)
        self.pos = pos
        self.rect = self.image.get_frect(topleft=self.pos)

        def click(self, *args):
            pass


class AkcjeShowButton(TextButton):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        button_group,
        tekst,
        font,
        font_size,
        font_color,
    ):
        super().__init__(
            width, height, color, pos, button_group, tekst, font, font_size, font_color
        )

    def click(self):
        return 1


class RekrutacjaShowButton(TextButton):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        button_group,
        tekst,
        font,
        font_size,
        font_color,
    ):
        super().__init__(
            width, height, color, pos, button_group, tekst, font, font_size, font_color
        )

    def click(self):
        return 0


class Recruit_sample:
    def __init__(self, ruch):
        self.ruch = ruch
        self.max_ruch = ruch


class Recruit(Button):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        jednostka,
        id,
        button_group,
        description,
    ) -> None:
        super().__init__(width, height, color, pos, button_group, description)
        self.jednostka = jednostka
        self.id = id
        self.count = 0

    def get_squad_info(self):
        info = {}
        info["color"] = Client().player.color
        info["owner"] = Client().player.name
        info["owner_id"] = Client().player.id
        info["pos"] = (5000, 5000)
        info["strategy"] = 0
        info["wzmocnienie"] = False
        info["team"] = Client().player.team
        info["jednostki"] = []
        jednostka = self.jednostka
        jednostka["array_pos"] = 3
        info["jednostki"].append(jednostka)
        return info

    def click(self):
        if Mapa().move_flag is None:
            self.count += 1
            info = self.get_squad_info()
            Mapa().move_flag = Squad(
                Mapa().army_group, info, None, Client().player.frakcja
            )
            r = Recruit_sample(7)
            Mapa().correct_moves = Mapa().possible_moves(
                Client().player.x, Client().player.y, r
            )
            Mapa().move_group.empty()
        elif Mapa().move_flag.tile is None and len(Mapa().move_flag) < 7:
            self.count += 1
            info = self.get_squad_info()
            s = Squad(Mapa().army_group, info, None, Client().player.frakcja)
            Mapa().move_flag += s
        else:
            return

    def draw(self, screen):
        text = AssetManager.get_font("consolas", 20).render(
            str(self.count), True, "white"
        )
        text_rect = text.get_frect(topleft=(self.pos[0] + 45, self.pos[1] + 40))
        screen.blit(self.image, self.rect)
        screen.blit(text, text_rect)
        self.display_cost(self.jednostka["cost"], screen, self.count)


class Rozkaz(Button):
    def __init__(
        self, width, height, color, pos, typ, button_group, description, image=None
    ):
        super().__init__(width, height, color, pos, button_group, description, image)
        self.typ = typ
        self.color = color

    def click(self):
        cooldown = self.typ + "_cooldown"
        if not Client().player.akcje[cooldown] and Client().validate_cost(
            AssetManager.get_akcje(self.typ, "koszt")
        ):

            Client().pay(AssetManager.get_akcje(self.typ, "koszt"))
            Client().player.akcjeMenager.applybuff(self.typ)
            Client().player.akcje[self.typ] += AssetManager.get_akcje(
                self.typ, "mnoznik"
            )
            Client().player.akcje[self.typ + "_cooldown"] = True

            print(Client().player.akcje)
            Mapa().calculate_income()

    def draw(self, screen):
        if Client().player.akcje[self.typ + "_cooldown"]:
            self.image.fill((100, 100, 100))
        else:
            self.image.fill(self.color)
        screen.blit(self.image, self.rect)
        self.display_cost(AssetManager.get_koszt(self.typ), screen)


class Upgrade(Button):
    def __init__(
        self, width, height, color, pos, typ, button_group, description, image=None
    ):
        super().__init__(width, height, color, pos, button_group, description, image)
        self.typ = typ
        self.level_font = AssetManager.get_font("consolas", 20)
        self.level = Client().player.akcje[typ]

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        Client().player.akcje[self.typ] = value
        self.level_surf = self.level_font.render(str(self.level), True, "white")
        self.level_rect = self.level_surf.get_rect(
            bottomleft=(self.pos[0] + 45, self.pos[1] + 26)
        )
        Mapa().calculate_income()

    def click(self):
        if self.level < AssetManager.get_akcje(
            self.typ, "maks_level"
        ) and Client().validate_cost(AssetManager.get_koszt(self.typ, self.level + 1)):
            Client().pay(AssetManager.get_koszt(self.typ, self.level + 1))
            self.level = self.level + 1
            Mapa().refresh()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.level != AssetManager.get_akcje(self.typ, "maks_level"):
            self.display_cost(AssetManager.get_koszt(self.typ, self.level + 1), screen)
        else:
            text = self.level_font.render("maks.", True, "white")
            screen.blit(
                text,
                text.get_frect(topleft=(self.pos[0] + 70, self.pos[1] + 25)),
            )
        screen.blit(self.level_surf, self.level_rect)


class Menu(Button):
    def __init__(self, width, height, color, pos, button_group, description) -> None:
        super().__init__(width, height, color, pos, button_group, description, "menu")

    def click(self):
        Flag().show = not Flag().show


class Surrender(Button):
    def __init__(
        self, width, height, color, pos, button_group, description, image=None
    ):
        super().__init__(width, height, color, pos, button_group, description, image)

    def click(self):
        Client().send_result(Client().name)


class Exit(Button):
    def __init__(self, width, height, color, pos, button_group, image=None):
        super().__init__(width, height, color, pos, button_group, image)

    def click(self):
        Client().ekran = 0
        Client().name = None
        Client().id = None
        Client().leave()


class SquadButtonDisplay:
    def __init__(self, width, height, color, pos, tekst=None):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_frect(midbottom=self.pos)
        self.tekst = tekst

    def event(self, mouse_pos, move_flag):
        if move_flag is None:
            return
        if self.rect.collidepoint(mouse_pos):
            self.click()

    def click(self):
        SquadDisplay().show = not SquadDisplay().show


class Wzmocnienie(SquadButtonDisplay):
    def __init__(self, width, height, color, pos, tekst=None):
        super().__init__(width, height, color, pos, tekst)

    def event(self, squad, mouse_pos, id):
        if squad is None:
            return
        if squad.owner_id != id:
            return
        if squad.ruch < 4:
            return
        if squad.wzmocnienie:
            return
        if self.rect.collidepoint(mouse_pos):
            squad.wzmocnienie = True
            squad.ruch -= 4


class Rotate(SquadButtonDisplay):
    def __init__(self, width, height, color, pos, image=None):
        super().__init__(width, height, color, pos)

    def event(self, squad, mouse_pos, id):
        if squad is None:
            return
        if squad.owner_id != id:
            return
        if self.rect.collidepoint(mouse_pos):
            self.rotate(squad)

    def rotate(self, squad):
        bufor = squad.wojownicy[0]

        if squad.wojownicy[2] is not None:
            squad.wojownicy[2].pos = 0
        squad.wojownicy[0] = squad.wojownicy[2]

        if squad.wojownicy[5] is not None:
            squad.wojownicy[5].pos = 2
        squad.wojownicy[2] = squad.wojownicy[5]

        if squad.wojownicy[6] is not None:
            squad.wojownicy[6].pos = 5
        squad.wojownicy[5] = squad.wojownicy[6]

        if squad.wojownicy[4] is not None:
            squad.wojownicy[4].pos = 6
        squad.wojownicy[6] = squad.wojownicy[4]

        if squad.wojownicy[1] is not None:
            squad.wojownicy[1].pos = 4
        squad.wojownicy[4] = squad.wojownicy[1]

        squad.wojownicy[1] = bufor
        if squad.wojownicy[1] is not None:
            squad.wojownicy[1].pos = 1


class Gamble(Button):
    def __init__(self, width, height, color, pos, button_group, image_name=None):
        super().__init__(
            width,
            height,
            color,
            pos,
            button_group,
            "Hazard: wydaj 10 za możliwość zyskania 20!!!",
            image_name,
        )
        self.cost = {
            "zloto": 10,
            "srebro": 0,
            "stal": 0,
            "food": 0,
            "medale": 0,
        }

    def click(self):
        if Client().player.gold >= 10:
            if random.randint(0, 3):
                Client().player.gold -= 10
            else:
                Client().player.gold += 10

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.display_cost(self.cost, screen)
