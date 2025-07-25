from .singleton import Singleton
import pygame
from projekt.assetMenager import AssetManager
from .pozycja import AttackPosition
from .narzedzia import pozycja_myszy_na_surface


class AttackDisplay(metaclass=Singleton):
    sasiedzi = [(1, 2), (0, 4), (0, 5), (3, 3), (1, 6), (2, 6), (4, 5)]
    niepar_angles = [(-1, 0), (-1, 1), (0, -1), (3, 3), (0, 1), (-1, -1), (1, 1)]
    par_angles = [(-1, -1), (-1, 0), (0, -1), (3, 3), (0, 1), (1, -1), (1, 1)]

    def __init__(self, width, height, pos, color):
        if hasattr(self, "_initialized"):
            return
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_frect(center=pos)
        self.font = AssetManager.get_font("consolas", 26)
        self.font_color = color
        self.show = False

    def update(self, attacker, defender, distance, x1, y1, x2, y2):
        self.show = True
        self.distance = distance
        attack_angle = (y2 - y1, x2 - x1)
        match (x1 % 2):
            case 0:
                angles = AttackDisplay.par_angles
            case 1:
                angles = AttackDisplay.niepar_angles
        i = 0
        id = 0
        for angle in angles:
            if angle == attack_angle:
                id = i
                break
            i += 1

        print(id)
        print(attack_angle)

        self.attacker = OddzialAttack(
            self.width / 2, self.height, attacker, id, AttackDisplay.sasiedzi
        )
        self.defender = OddzialDefend(
            self.width / 2,
            self.height,
            defender,
            6 - id,
            AttackDisplay.sasiedzi,
        )

    def display(self, screen):
        self.surf.fill("white")
        self.attacker.draw(self.surf)
        self.defender.draw(self.surf)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        AttackDisplay().ifselected = False
        self.defender.event(mouse_pos)
        self.attacker.event(mouse_pos)

    def hover(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        self.attacker.hover(mouse_pos)
        self.defender.hover(mouse_pos)


class Oddzial:
    def __init__(self, width, height, squad, id, sasiedzi):
        self.surf = pygame.Surface((width, height))
        self.surf.fill("white")
        self.rect = self.surf.get_frect(topleft=(0, 0))
        self.squad = squad
        self.load_lines(sasiedzi, id)
        self.pozycje_group = pygame.sprite.Group()
        self.load_positions()
        self.load_army()

    def load_lines(self, sasiedzi, id):
        self.firstline = []
        self.firstline.append(sasiedzi[id][0])
        self.firstline.append(3)
        self.firstline.append(id)
        self.firstline.append(sasiedzi[id][1])
        self.secondline = []
        for i in range(0, 7):
            if i not in self.firstline:
                self.secondline.append(i)
        self.selected = None

    def load_positions(self):
        i = 0
        for pozycja in self.pozycje:
            AttackPosition(pozycja, (0, 0), 50, 50, self.pozycje_group, 1, i)
            i += 1

    def load_army(self):
        i = 0
        for pozycja in self.pozycje_group:
            if i < 3:
                pozycja.wojownik = self.squad.wojownicy[self.secondline[i]]
                if self.squad.wojownicy[self.secondline[i]] is not None:
                    pozycja.id = self.squad.wojownicy[self.secondline[i]].pos
            else:
                pozycja.wojownik = self.squad.wojownicy[self.firstline[i - 3]]
                if self.squad.wojownicy[self.firstline[i - 3]] is not None:
                    pozycja.id = self.squad.wojownicy[self.firstline[i - 3]].pos
            i += 1

    def draw(self, screen):
        self.surf.fill("white")
        for pozycja in self.pozycje_group:
            pozycja.display(self.surf, self.squad.color)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        for pozycja in self.pozycje_group:
            if pozycja.rect.collidepoint(mouse_pos):
                AttackDisplay().selected = pozycja
                pozycja.color = (200, 200, 200)
                AttackDisplay().ifselected = True
            else:
                pozycja.color = "white"
        if not AttackDisplay().ifselected:
            AttackDisplay().selected = None
        else:
            AttackDisplay().selected.color = (200, 200, 200)

    def hover(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        for pozycja in self.pozycje_group:
            pozycja.hover(mouse_pos)


class OddzialAttack(Oddzial):
    def __init__(self, width, height, squad, id, sasiedzi):
        self.pozycje = [
            (width / 5 * 1, height / 5 * 2),
            (width / 5 * 1, height / 5 * 3),
            (width / 5 * 1, height / 5 * 4),
            (width / 5 * 3, height / 5 * 2),
            (width / 5 * 3, height / 5 * 2.7),
            (width / 5 * 3, height / 5 * 3.3),
            (width / 5 * 3, height / 5 * 4),
        ]
        super().__init__(width, height, squad, id, sasiedzi)


class OddzialDefend(Oddzial):
    def __init__(self, width, height, squad, id, sasiedzi):
        self.pozycje = [
            (width / 5 * 4, height / 5 * 2),
            (width / 5 * 4, height / 5 * 3),
            (width / 5 * 4, height / 5 * 4),
            (width / 5 * 2, height / 5 * 2),
            (width / 5 * 2, height / 5 * 2.7),
            (width / 5 * 2, height / 5 * 3.3),
            (width / 5 * 2, height / 5 * 4),
        ]
        super().__init__(width, height, squad, id, sasiedzi)
        self.rect = self.surf.get_frect(topright=(width * 2, 0))

    def event(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
            for pozycja in self.pozycje_group:
                if (
                    pozycja.rect.collidepoint(mouse_pos)
                    and AttackDisplay().selected is not None
                    and AttackDisplay().selected.wojownik.atak_points > 0
                    and pozycja.wojownik is not None
                ):
                    damage = AttackDisplay().selected.wojownik.bronie[0]["atak"]
                    AttackDisplay().selected.wojownik.atak_points -= (
                        AttackDisplay().selected.wojownik.bronie[0]["koszt_ataku"]
                    )
                    self.squad.zdrowie(pozycja.id, pozycja.wojownik.zdrowie - damage)
                    pozycja.wojownik = self.squad.wojownicy[pozycja.id]
                    AttackDisplay().ifselected = True
