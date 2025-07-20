import pygame
from .narzedzia import pozycja_myszy_na_surface, oslab_kolor


class AttackDisplay:
    def __init__(self, width, height, pos, color):
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_frect(center=pos)
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", int(self.width / 30))
        self.font_color = color
        self.show = False

    def update(self, attacker, defender, distance):
        self.show = True
        self.attacker = attacker
        self.defender = defender
        self.distance = distance

        self.attackers_surfs = SurfAttack(
            self.width / 2 - 1, self.height, (0, 0), self.attacker, distance
        )
        self.defenders_surfs = SurfDefend(
            self.width / 2 - 1,
            self.height,
            (self.width, 0),
            self.defender,
        )

    def display(self, screen):
        self.surf.fill("white")
        self.attackers_surfs.display(self.surf, (self.rect.x, self.rect.y))
        pygame.draw.line(
            self.surf, "black", (self.width / 2, 0), (self.width / 2, self.height), 1
        )
        self.defenders_surfs.display(self.surf, (self.rect.x, self.rect.y))

        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos):
        self.attackers_surfs.event(
            pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y)),
        )
        self.defenders_surfs.event(
            pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y)),
            self.attackers_surfs.selected,
        )


class SurfOddzialu:
    def __init__(self, width, height, pos, squad):
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_frect(topleft=pos)
        self.pos = pos
        self.squad = squad
        self.surfs = []
        self.create_surf()
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", int(self.width / 15))
        self.font_color = "black"

    def create_surf(self):
        surfaces = []
        i = 1
        for wojownik in self.squad.wojownicy:
            surfaces.append(
                WojownikSurfAttack(
                    self.width,
                    self.squad,
                    i - 1,
                    wojownik,
                    (5, 50 + i * 26),
                    i,
                    self.squad.color,
                )
            )
            if self.surfs[i - 1].selected:
                surfaces[i - 1].selected = True
            i += 1

        self.surfs = surfaces

    def display(self, screen, origin):
        self.surf.fill("white")
        self.create_surf()
        display = self.squad.display(0)
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=(20, 20))
        self.surf.blit(text, text_rect)

        for surf in self.surfs:
            surf.display(self.surf, self.pos, origin, self.squad.color)
        screen.blit(self.surf, self.rect)


class SurfAttack(SurfOddzialu):
    def __init__(self, width, height, pos, squad, distance):
        super().__init__(width, height, pos, squad)
        self.rect = self.surf.get_frect(topleft=pos)
        self.distance = distance
        self.selected = None

    def create_surf(self):
        surfaces = []
        i = 1
        for wojownik in self.squad.wojownicy:
            if wojownik is None:
                continue
            surfaces.append(
                WojownikSurfAttack(
                    self.width,
                    self.squad,
                    i - 1,
                    wojownik,
                    (5, 50 + i * int(self.width / 15)),
                    wojownik.pos,
                    self.squad.color,
                )
            )
            if len(self.surfs) > 0:
                if self.surfs[i - 1].selected:
                    surfaces[i - 1].selected = True
            i += 1

        self.surfs = surfaces

    def event(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
            self.selected = None
            for surf in self.surfs:
                surf.selected = False
            for surf in self.surfs:
                if (
                    surf.rect.collidepoint(mouse_pos)
                    and surf.jednostka.bronie[0]["range"] >= self.distance
                ):
                    self.selected = surf.jednostka
                    surf.selected = True
                    return

    def display(self, screen, origin):
        self.surf.fill("white")
        self.create_surf()
        display = self.squad.display(0)
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=(20, 20))
        self.surf.blit(text, text_rect)

        for surf in self.surfs:
            if surf.jednostka.bronie[0]["range"] < self.distance:
                surf.display(self.surf, self.pos, origin, "grey")
            else:
                surf.display(self.surf, self.pos, origin, self.squad.color)
        screen.blit(self.surf, self.rect)


class SurfDefend(SurfOddzialu):
    def __init__(self, width, height, pos, squad):
        super().__init__(width, height, pos, squad)
        self.rect = self.surf.get_frect(topright=pos)

    def create_surf(self):
        self.surfs = []

        i = 1
        if not self.squad is None:
            for wojownik in self.squad.wojownicy:
                if wojownik is None:
                    continue
                self.surfs.append(
                    WojownikSurfDefend(
                        self.width,
                        self.squad,
                        i - 1,
                        wojownik,
                        (self.width - 5, 50 + i * int(self.width / 15)),
                        wojownik.pos,
                        self.squad.color,
                    )
                )
                i += 1

    def display(self, screen, origin):
        self.surf.fill("white")
        self.create_surf()
        if not self.squad is None:
            display = self.squad.display(0)
        elif not self.budynek is None:
            display = self.budynek.owner_display()
        else:
            display = "Zniszczone miasto"
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topright=(self.width - 20, 20))
        self.surf.blit(text, text_rect)

        for surf in self.surfs:
            surf.display(
                self.surf, (self.rect.x, self.rect.y), origin, self.squad.color
            )
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos, selected):
        flag = True
        if selected is None:
            return
        if self.rect.collidepoint(mouse_pos):
            flag = False
            for surf in self.surfs:
                surf.event(
                    selected,
                    pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y)),
                )
                if not surf.budynek is None:
                    flag = True
        if not flag:
            self.budynek = None


class WojownikSurf:
    def __init__(self, width, squad, poz, jednostka, pos, id, color):
        self.width = width
        self.id = id
        self.squad = squad
        self.poz = poz
        self.surf = pygame.Surface(
            (self.width - 30, int(self.width / 20)), pygame.SRCALPHA
        )
        self.rect = self.surf.get_frect(topleft=pos)
        self.jednostka = jednostka
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", int(self.width / 35))
        self.font_color = "black"
        self.color = color

    def display(self, screen, pos, origin, color):
        self.surf.fill("white")
        self.hover(pos, origin, pygame.mouse.get_pos(), color)
        display = self.jednostka.display(self.id)
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=(15, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, color, self.rect, 1)

    def hover(self, pos, origin, mouse_pos, color):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, origin)
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, pos)
        if self.rect.collidepoint(mouse_pos) and color != "grey":
            self.surf.fill(oslab_kolor(pygame.Color(color), 20))


class WojownikSurfAttack(WojownikSurf):
    def __init__(self, width, squad, poz, jednostka, pos, id, color):
        super().__init__(width, squad, poz, jednostka, pos, id, color)
        self.rect = self.surf.get_frect(topleft=pos)
        self.selected = False

    def display(self, screen, pos, origin, color):
        self.surf.fill("white")
        self.hover(pos, origin, pygame.mouse.get_pos(), color)
        display = self.jednostka.display(self.id)
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topleft=(15, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
        width = 1
        if self.selected:
            width = 4

        pygame.draw.rect(screen, color, self.rect, width)


class WojownikSurfDefend(WojownikSurf):
    def __init__(self, width, squad, poz, jednostka, pos, id, color):
        super().__init__(width, squad, poz, jednostka, pos, id, color)
        self.rect = self.surf.get_frect(topright=pos)
        self.pos = pos
        self.budynek = None

    def display(self, screen, pos, origin, color):
        self.surf.fill("white")
        self.hover(pos, origin, pygame.mouse.get_pos(), color)
        display = self.jednostka.display(self.id)
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topright=(self.width - 45, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, color, self.rect, 1)

    def event(self, selected, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if selected.atak_points > 0:
                selected.atak_points -= selected.bronie[0]["koszt_ataku"]
                self.squad.zdrowie(
                    self.jednostka.pos,
                    self.jednostka.zdrowie - selected.bronie[0]["atak"],
                )


"""
class BudynekSurfDefend(WojownikSurf):
    def __init__(self, width, budynek, pos):
        self.width = width
        self.surf = pygame.Surface(
            (self.width - 30, int(self.width / 20)), pygame.SRCALPHA
        )
        self.rect = self.surf.get_frect(topright=pos)
        self.budynek = budynek
        self.font = pygame.font.Font("Grafika/fonts/consolas.ttf", int(self.width / 35))
        self.font_color = "black"

    def display(self, screen, pos, origin):
        self.surf.fill("white")
        self.hover(pos, origin, pygame.mouse.get_pos())
        display = self.budynek.display()
        text = self.font.render(display, True, self.font_color)
        text_rect = text.get_rect(topright=(self.width - 45, 5))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, self.budynek.color, self.rect, 1)

    def hover(self, pos, origin, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, origin)
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, pos)
        if self.rect.collidepoint(mouse_pos):
            self.surf.fill(oslab_kolor(pygame.Color(self.budynek.color), 20))

    def event(self, selected, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if selected.atak_points > 0:
                self.budynek.zdrowie -= selected.atak
                selected.atak_points -= selected.koszt_ataku
                if self.budynek.zdrowie <= 0:
                    print("None")
                    self.budynek = None
"""
