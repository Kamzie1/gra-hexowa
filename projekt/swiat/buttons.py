from projekt.jednostki import Squad
import pygame
from os.path import join


class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        width,
        height,
        color,
        pos,
        button_group,
        image=None,
    ) -> None:
        super().__init__(button_group)
        if image is None:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            self.image = pygame.image.load(f"Grafika/{image}")
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
        self.font = pygame.font.Font(join("Grafika/fonts", font), font_size)
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
        self.font = pygame.font.Font(join("Grafika/fonts", "consolas.ttf"), 10)
        self.gold_icon = pygame.image.load(join("Grafika", "złoto.png"))
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
        info["jednostki"].append(jednostka)
        self.mapa.move_flag = Squad(self.group, info, None, self.player.frakcja)
        r = Recruit_sample(4)
        self.mapa.correct_moves = self.mapa.possible_moves(self.x, self.y, r)
        self.mapa.move_group.empty()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.scaled_gold_icon, self.gold_rect)
        screen.blit(self.text, self.text_rect)


class Menu(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group, "menu.png")

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
