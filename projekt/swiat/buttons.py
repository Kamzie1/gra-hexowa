from projekt.jednostki import Squad
import pygame
from os.path import join
from projekt.dane import Akcje
from projekt.assetMenager import AssetManager


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        button_group,
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

    def click(self, *args):
        pass


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
        self.font = AssetManager.get_font("consolas", 24)
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


class Recruit(Button):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        jednostka,
        id,
        group,
        button_group,
        recruit_pos,
        player,
        mapa,
        x,
        y,
    ) -> None:
        super().__init__(width, height, color, pos, button_group)
        self.group = group
        self.recruit_pos = recruit_pos
        self.jednostka = jednostka
        self.id = id
        self.player = player
        self.mapa = mapa
        self.x = x
        self.y = y
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
        info["color"] = self.player.color
        info["owner"] = self.player.name
        info["owner_id"] = self.player.id
        info["pos"] = (5000, 5000)
        info["jednostki"] = []
        jednostka = self.jednostka
        jednostka["array_pos"] = 3
        info["jednostki"].append(jednostka)
        self.mapa.move_flag = Squad(self.group, info, None, self.player.frakcja)
        r = Recruit_sample(4)
        self.mapa.correct_moves = self.mapa.possible_moves(self.x, self.y, r)
        self.mapa.move_group.empty()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.text, self.text_rect)


class Rozkaz(Button):
    def __init__(
        self, width, height, color, pos, type, button_group, player, image=None
    ):
        super().__init__(width, height, color, pos, button_group, image)
        self.player = player
        self.type = type
        self.font = AssetManager.get_font("consolas", 10)
        self.gold_icon = AssetManager.get_asset("złoto")
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))
        self.gold_rect = self.scaled_gold_icon.get_frect(
            topleft=(pos[0] + 45, pos[1] + 5)
        )
        self.display = f"{Akcje[type]["koszt"]["gold"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(topleft=(pos[0] + 60, pos[1] + 10))

    def click(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.text, self.text_rect)


class Upgrade(Button):
    def __init__(
        self, width, height, color, pos, type, button_group, player, level, image=None
    ):
        super().__init__(width, height, color, pos, button_group, image)
        self.player = player
        self.type = type
        self.font = AssetManager.get_font("consolas", 10)
        self.level_font = AssetManager.get_font("consolas", 16)
        self.gold_icon = AssetManager.get_asset("złoto")
        self.scaled_gold_icon = pygame.transform.scale(self.gold_icon, (20, 20))
        self.gold_rect = self.scaled_gold_icon.get_frect(
            topleft=(pos[0] + 45, pos[1] + 5)
        )
        self.level = level
        self.display = f"{Akcje[self.type][self.level -1]["koszt"]["gold"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(topleft=(pos[0] + 60, pos[1] + 10))

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value
        self.display = f"{Akcje[self.type][self._level -1]["koszt"]["gold"]}"
        self.text = self.font.render(self.display, True, "white")
        self.text_rect = self.text.get_rect(
            topleft=(self.pos[0] + 60, self.pos[1] + 10)
        )
        self.level_surf = self.level_font.render(str(self.level), True, "white")
        self.level_rect = self.level_surf.get_rect(
            bottomleft=(self.pos[0] + 30, self.pos[1] + 20)
        )

    def click(self):
        print(self.level)
        if self.level < 3:
            print(self.level, " je")
            self.level = self.level + 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.level_surf, self.level_rect)
        screen.blit(self.text, self.text_rect)


class Menu(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group, "menu")

    def click(self, flag):
        flag.show = not flag.show


class Surrender(Button):
    def __init__(self, width, height, color, pos, button_group, image=None):
        super().__init__(width, height, color, pos, button_group, image)

    def click(self, client, koniecGry):
        client.end_game(-1, koniecGry)


class SquadButtonDisplay:
    def __init__(self, width, height, color, pos, tekst=None):
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_frect(midbottom=self.pos)
        self.tekst = tekst

    def event(self, mouse_pos, squadDisplay, move_flag):
        if move_flag is None:
            return
        if self.rect.collidepoint(mouse_pos):
            self.click(squadDisplay)

    def click(self, squadDisplay):
        squadDisplay.show = not squadDisplay.show


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
