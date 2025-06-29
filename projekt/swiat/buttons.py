from projekt.jednostki import Squad
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, color, pos, button_group, image=None) -> None:
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
        r = Recruit_sample(2)
        self.mapa.correct_moves = self.mapa.possible_moves(self.x, self.y, r)
        self.mapa.move_group.empty()


class Menu(Button):
    def __init__(self, width, height, color, pos, button_group) -> None:
        super().__init__(width, height, color, pos, button_group, "menu.png")

    def click(self, flag):
        flag.show = not flag.show


class Surrender(Button):
    def __init__(self, width, height, color, pos, button_group, image=None):
        super().__init__(width, height, color, pos, button_group, image)

    def click(self, client):
        client.send_result(client.name)


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
