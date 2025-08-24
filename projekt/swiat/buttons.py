from projekt.jednostki import Squad
import pygame
from os.path import join
from projekt.assetMenager import AssetManager
from .squadDisplay import SquadDisplay
from .mapa import Mapa
from projekt.network import Client
from projekt.akcjeMenager import AkcjeMenager
from projekt.flag import Flag


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


class TextButton(pygame.sprite.Sprite):
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
        self.font = AssetManager.get_font("consolas", 10)
        self.gold_icon = AssetManager.get_asset("złoto")
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))
        self.gold_rect = self.scaled_gold_icon.get_frect(
            topleft=(pos[0] + 45, pos[1] + 5)
        )
        self.display = f"{jednostka["cost"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(topleft=(pos[0] + 60, pos[1] + 10))

    def click(self):
        info = {}
        info["color"] = Client().player.color
        info["owner"] = Client().player.name
        info["owner_id"] = Client().player.id
        info["pos"] = (5000, 5000)
        info["strategy"] = 0
        info["jednostki"] = []
        jednostka = self.jednostka
        jednostka["array_pos"] = 3
        info["jednostki"].append(jednostka)
        Mapa().move_flag = Squad(Mapa().army_group, info, None, Client().player.frakcja)
        r = Recruit_sample(7)
        Mapa().correct_moves = Mapa().possible_moves(
            Client().player.x, Client().player.y, r
        )
        Mapa().move_group.empty()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.text, self.text_rect)


class Rozkaz(Button):
    def __init__(
        self, width, height, color, pos, typ, button_group, description, image=None
    ):
        super().__init__(width, height, color, pos, button_group, description, image)
        self.typ = typ
        self.font = AssetManager.get_font("consolas", 10)
        self.gold_icon = AssetManager.get_asset("złoto")
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))
        self.gold_rect = self.scaled_gold_icon.get_frect(
            topleft=(pos[0] + 45, pos[1] + 5)
        )
        self.display = f"{AssetManager.get_koszt(self.typ)["gold"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(topleft=(pos[0] + 60, pos[1] + 10))
        self.color = color

    def click(self):
        cooldown = self.typ + "_cooldown"
        if not Client().player.akcje[cooldown]:
            try:
                Client().player.gold -= AssetManager.get_akcje(self.typ, "koszt")[
                    "gold"
                ]
            except:
                print("not enough money")
            else:
                Client().player.akcjeMenager.applybuff(self.typ)
                Client().player.akcje[self.typ] += AssetManager.get_akcje(
                    self.typ, "mnoznik"
                )
                Client().player.akcje[self.typ + "_cooldown"] = True

                Mapa().calculate_income()
                Mapa().refresh_movement(
                    Client().users[Client().player.id]["akcje"]["movement_rozkaz"],
                    Client().player.id,
                )

    def draw(self, screen):
        if Client().player.akcje[self.typ + "_cooldown"]:
            self.image.fill((100, 100, 100))
        else:
            self.image.fill(self.color)
        screen.blit(self.image, self.rect)
        screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.text, self.text_rect)


class Upgrade(Button):
    def __init__(
        self, width, height, color, pos, typ, button_group, description, image=None
    ):
        super().__init__(width, height, color, pos, button_group, description, image)
        self.typ = typ
        self.font = AssetManager.get_font("consolas", 10)
        self.level_font = AssetManager.get_font("consolas", 16)
        self.gold_icon = AssetManager.get_asset("złoto")
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))
        self.gold_rect = self.scaled_gold_icon.get_frect(
            topleft=(pos[0] + 45, pos[1] + 5)
        )
        self.level = Client().player.akcje[typ]
        self.display = f"{AssetManager.get_koszt(self.typ, self.level+1)["gold"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(topleft=(pos[0] + 60, pos[1] + 10))

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        Client().player.akcje[self.typ] = value
        self.display = f"{AssetManager.get_koszt(self.typ, self.level+1)["gold"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(
            topleft=(self.pos[0] + 60, self.pos[1] + 10)
        )
        self.level_surf = self.level_font.render(str(self.level), True, "white")
        self.level_rect = self.level_surf.get_rect(
            bottomleft=(self.pos[0] + 30, self.pos[1] + 20)
        )
        Mapa().calculate_income()

    def click(self):
        if self.level < 4:
            try:
                Client().player.gold -= AssetManager.get_koszt(
                    self.typ, self.level + 1
                )["gold"]
            except:
                print("not enough money")
            else:
                self.level = self.level + 1
                Mapa().refresh()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.level != len(AssetManager.get_akcje(self.typ)) - 1:
            screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.level_surf, self.level_rect)
        screen.blit(self.text, self.text_rect)


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
