from projekt.narzedzia import (
    Singleton,
    AttackPosition,
    pozycja_myszy_na_surface,
    Przycisk,
    Switch,
    pos_on_screen,
)
import pygame
from projekt.assetMenager import AssetManager
import random
from projekt.animationMenager import AnimationMenager
from projekt.network import Client
from projekt.jednostki import Wojownik
from time import sleep


class AttackDisplay(metaclass=Singleton):
    sasiedzi = [(1, 2), (0, 4), (0, 5), (0, 0), (1, 6), (2, 6), (4, 5)]
    niepar_angles = [(-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (-1, -1), (1, 1)]
    par_angles = [(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1), (1, -1), (1, 1)]

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
        self.defender = None
        self.turn = "Pierwsza Linia"
        self.atakButton = Przycisk(
            120, 40, "red", (self.width / 2, self.height / 4), "atakuj", "white"
        )
        self.strategies = [
            "strategia: najsłabszy",
            "strategia: najsilniejszy",
            "strategia: lord/max",
            "strategia: lord/min",
        ]
        self.atakStrategy = Switch(
            300, 32, (self.width / 4, self.height / 4), self.strategies
        )
        self.selected = None

    def update(
        self, attacker, defender, distance, x1, y1, x2, y2, defense1, defense2, pogoda
    ):
        self.show = True
        self.distance = distance
        self.turn = 1
        self.pogoda = pogoda
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

        self.attacker = OddzialAttack(
            self.width / 2,
            self.height,
            attacker,
            id,
            AttackDisplay.sasiedzi,
            distance,
            defense1,
        )
        self.defender = OddzialDefend(
            self.width / 2,
            self.height,
            defender,
            6 - id,
            AttackDisplay.sasiedzi,
            distance,
            defense2,
        )

    def display(self, screen):
        self.surf.fill("green")
        self.attacker.draw(self.surf)
        self.defender.draw(self.surf)
        self.atakButton.draw(self.surf)
        self.atakStrategy.draw(self.attacker.squad.strategy, self.surf)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        AttackDisplay().ifselected = False
        if self.atakStrategy.rect.collidepoint(mouse_pos):
            self.attacker.squad.strategy += 1
            self.attacker.squad.strategy %= len(self.strategies)
        if self.atakButton.rect.collidepoint(mouse_pos):
            self.automate_atak()
        self.defender.event(mouse_pos)
        self.attacker.event(mouse_pos)

    def automate_atak(self):
        self.stop = False
        self.target = self.get_target(
            self.defender.pozycje_group, self.attacker.squad.strategy
        )
        if self.target is None:
            return
        while self.active_pozycje():
            self.defender.defender_update_positions()
            self.target = self.get_target(
                self.defender.pozycje_group, self.attacker.squad.strategy
            )
            if self.target is None:
                return
            self.do_atak(self.attacker, self.defender)
            if self.stop:
                return
            self.attacker.defender_update_positions()
            self.defender.attacker_update_positions()
            self.target = self.get_target(
                self.attacker.pozycje_group, self.defender.squad.strategy
            )
            if self.target is None:
                return
            self.do_atak(self.defender, self.attacker)
            if self.stop:
                return
            self.attacker.attacker_update_positions()
        self.defender.update_atak_points()

    def active_pozycje(self):
        for pozycja in self.attacker.pozycje_group:
            if pozycja.active:
                return True

        for pozycja in self.defender.pozycje_group:
            if pozycja.active:
                return True
        return False

    def load_min_wojownik(self):
        return Wojownik(
            Client().player.frakcja["jednostka"][0], 0, "jednostka", "red", 0, 0, 0, 0
        )

    def load_max_wojownik(self):
        return Wojownik(
            Client().player.frakcja["specjalne"][0],
            0,
            "specjalne",
            "red",
            1000,
            1000,
            1000,
            0,
        )

    def get_target(self, pozycje, strategy):
        max_wojownik = self.load_min_wojownik()
        min_wojownik = self.load_max_wojownik()
        lord_max = self.load_min_wojownik()
        lord_min = self.load_max_wojownik()
        wybrany = False
        lord_wybrany = False
        pozycja_min, pozycja_max, pozycja_lord_max, pozycja_lord_min = (
            None,
            None,
            None,
            None,
        )
        for pozycja in pozycje:
            if not pozycja.active or pozycja.wojownik is None:
                continue
            wybrany = True
            if pozycja.wojownik.damage_score() > max_wojownik.damage_score():
                max_wojownik = pozycja.wojownik
                pozycja_max = pozycja
            if pozycja.wojownik.health_score() < min_wojownik.health_score():
                min_wojownik = pozycja.wojownik
                pozycja_min = pozycja
            if pozycja.wojownik.lord:
                if pozycja.wojownik.damage_score() > lord_max.damage_score():
                    lord_wybrany = True
                    lord_max = pozycja.wojownik
                    pozycja_lord_max = pozycja
                if pozycja.wojownik.health_score() > lord_min.health_score():
                    lord_wybrany = True
                    lord_min = pozycja.wojownik
                    pozycja_lord_min = pozycja

        if not wybrany:
            return None

        match (strategy):
            case 0:
                return pozycja_min
            case 1:
                return pozycja_max
            case 2:
                if lord_wybrany:
                    return pozycja_lord_max
                return pozycja_max
            case 3:
                if lord_wybrany:
                    return pozycja_lord_min
                return pozycja_min

    def do_atak(self, attacker, defender):
        for pozycja in attacker.pozycje_group:
            if pozycja.active:
                self.selected = pozycja
                self.atak_pozycja(
                    self.target,
                    defender.squad,
                    (defender.rect.x, defender.rect.y),
                    defender.defense,
                )
                if self.target.wojownik is None:
                    self.target = self.get_target(
                        defender.pozycje_group, attacker.squad.strategy
                    )
                    if self.target is None:
                        self.stop = True
                        return

    def hover(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        self.attacker.hover(mouse_pos)
        self.defender.hover(mouse_pos)

    def calculateDamage(self, wojownik, defense, buff, owner_id):
        attacker = self.selected.wojownik
        self.selected.wojownik.atak_points -= self.selected.wojownik.bronie[0][
            "koszt_ataku"
        ]
        defense_buff = wojownik.pancerz - attacker.bronie[0]["przebicie"]
        rzut = random.randint(0, 50)
        rzut += random.randint(0, 50)
        if defense_buff > 0:
            rzut -= defense_buff
        if self.pogoda == 3 and wojownik.bronie[0]["typ"] == "prochowa":
            if not random.randint(0, 2):
                return 0
        if rzut > defense * 100 + buff:
            atak = random.randint(
                attacker.bronie[0]["atak"][0], attacker.bronie[0]["atak"][1]
            )
            if atak > wojownik.zdrowie:
                if owner_id == Client().player.id:
                    Client().player.medals += 5
                else:
                    Client().users[owner_id]["medals"] += 5
            else:
                if owner_id == Client().player.id:
                    Client().player.medals += 1
                else:
                    Client().users[owner_id]["medals"] += 1
            return atak
        return 0

    def atak_pozycja(self, pozycja, squad, pos, defense):
        if squad.wzmocnienie:
            buff = 5
        else:
            buff = 0
        damage = self.calculateDamage(pozycja.wojownik, defense, buff, squad.owner_id)
        squad.zdrowie(pozycja.id, pozycja.wojownik.zdrowie - damage)
        pozycja.wojownik = squad.wojownicy[pozycja.id]
        self.ifselected = True
        animation = (
            60,
            0,
            str(damage),
            pos_on_screen(
                (pozycja.pos[0] + 70, pozycja.pos[1] - 30),
                pos,
                (self.rect.x, self.rect.y),
            ),
        )
        AnimationMenager.animations.append(animation)
        if (
            int(
                self.selected.wojownik.atak_points
                / self.selected.wojownik.bronie[0]["koszt_ataku"]
            )
            <= 0
        ):
            self.selected.active = False
            self.ifselected = False


class Oddzial:
    def __init__(self, width, height, squad, id, sasiedzi, distance, defense):
        self.surf = pygame.Surface((width, height))
        self.defense = defense
        self.distance = distance
        self.surf.fill("white")
        self.rect = self.surf.get_frect(topleft=(0, 0))
        self.squad = squad
        self.load_lines(sasiedzi, id)
        self.pozycje_group = pygame.sprite.Group()
        self.load_positions()

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

    def load_atak_army(self):
        i = 0
        for pozycja in self.pozycje_group:
            if i < 3:
                pozycja.wojownik = self.squad.wojownicy[self.secondline[i]]
                pozycja.line = 2
                if (
                    self.distance == 1
                    and self.squad.wojownicy[self.firstline[i]] is not None
                ):
                    pozycja.active = False
                else:
                    if self.squad.wojownicy[self.secondline[i]] is not None:
                        pozycja.id = self.squad.wojownicy[self.secondline[i]].pos
                        if (
                            int(
                                pozycja.wojownik.atak_points
                                / pozycja.wojownik.bronie[0]["koszt_ataku"]
                            )
                            > 0
                            and pozycja.wojownik.bronie[0]["range"] >= self.distance
                        ):
                            pozycja.active = True
                        else:
                            pozycja.active = False
                    else:
                        pozycja.active = False

            else:
                pozycja.wojownik = self.squad.wojownicy[self.firstline[i - 3]]
                pozycja.line = 1
                if self.squad.wojownicy[self.firstline[i - 3]] is not None:
                    pozycja.id = self.squad.wojownicy[self.firstline[i - 3]].pos
                    if (
                        int(
                            pozycja.wojownik.atak_points
                            / pozycja.wojownik.bronie[0]["koszt_ataku"]
                        )
                        > 0
                        and self.distance <= pozycja.wojownik.bronie[0]["range"]
                    ):
                        pozycja.active = True
                    else:
                        pozycja.active = False
                else:
                    pozycja.active = False
            i += 1

    def load_defend_army(self):
        i = 0
        for pozycja in self.pozycje_group:
            if i < 3:
                pozycja.wojownik = self.squad.wojownicy[self.secondline[i]]
                pozycja.line = 2
                if self.distance == 1:
                    pozycja.active = False
                else:
                    if self.squad.wojownicy[self.secondline[i]] is not None:
                        pozycja.id = self.squad.wojownicy[self.secondline[i]].pos
                        pozycja.active = True
                    else:
                        pozycja.active = False

            else:
                pozycja.wojownik = self.squad.wojownicy[self.firstline[i - 3]]
                pozycja.line = 1
                if self.squad.wojownicy[self.firstline[i - 3]] is not None:
                    pozycja.id = self.squad.wojownicy[self.firstline[i - 3]].pos
                    pozycja.active = True
                else:
                    pozycja.active = False
            i += 1

    def defender_update_positions(self):
        i = 0
        for pozycja in self.pozycje_group:
            if i < 3:
                if self.distance == 1:
                    pozycja.active = False
                else:
                    if self.squad.wojownicy[self.secondline[i]] is not None:
                        pozycja.active = True
                    else:
                        pozycja.active = False

            else:
                if self.squad.wojownicy[self.firstline[i - 3]] is not None:
                    pozycja.active = True
                else:
                    pozycja.active = False
            i += 1

    def attacker_update_positions(self):
        i = 0
        for pozycja in self.pozycje_group:
            if i < 3:
                if (
                    self.distance == 1
                    and self.squad.wojownicy[self.firstline[i]] is not None
                ):
                    pozycja.active = False
                else:
                    if self.squad.wojownicy[self.secondline[i]] is not None:
                        if (
                            int(
                                pozycja.wojownik.atak_points
                                / pozycja.wojownik.bronie[0]["koszt_ataku"]
                            )
                            > 0
                            and pozycja.wojownik.bronie[0]["range"] >= self.distance
                        ):
                            pozycja.active = True
                        else:
                            pozycja.active = False
                    else:
                        pozycja.active = False

            else:
                if self.squad.wojownicy[self.firstline[i - 3]] is not None:
                    if (
                        int(
                            pozycja.wojownik.atak_points
                            / pozycja.wojownik.bronie[0]["koszt_ataku"]
                        )
                        > 0
                        and self.distance <= pozycja.wojownik.bronie[0]["range"]
                    ):
                        pozycja.active = True
                    else:
                        pozycja.active = False
                else:
                    pozycja.active = False
            i += 1

    def draw(self, screen):
        self.surf.fill("white")
        for pozycja in self.pozycje_group:
            pozycja.display(self.surf, self.squad.color)
        if self.squad.wzmocnienie:
            text = AssetManager.get_font("consolas", 20).render(
                f"obrona: {self.defense*100 + 5}%", True, "black"
            )
        else:
            text = AssetManager.get_font("consolas", 20).render(
                f"obrona: {self.defense*100}%", True, "black"
            )
        text_rect = text.get_frect(topleft=(100, 50))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)

    def event(self, mouse_pos):
        mouse_pos = pozycja_myszy_na_surface(mouse_pos, (self.rect.x, self.rect.y))
        for pozycja in self.pozycje_group:
            if pozycja.rect.collidepoint(mouse_pos):
                if pozycja.active:
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
            if pozycja.active:
                pozycja.hover(mouse_pos)


class OddzialAttack(Oddzial):
    def __init__(self, width, height, squad, id, sasiedzi, distance, defense):
        self.pozycje = [
            (width / 5 * 1, height / 5 * 2),
            (width / 5 * 1, height / 5 * 3),
            (width / 5 * 1, height / 5 * 4),
            (width / 5 * 3, height / 5 * 2),
            (width / 5 * 3, height / 5 * 2.7),
            (width / 5 * 3, height / 5 * 3.3),
            (width / 5 * 3, height / 5 * 4),
        ]
        super().__init__(width, height, squad, id, sasiedzi, distance, defense)
        self.load_atak_army()


class OddzialDefend(Oddzial):
    def __init__(self, width, height, squad, id, sasiedzi, distance, defense):
        self.pozycje = [
            (width / 5 * 4, height / 5 * 2),
            (width / 5 * 4, height / 5 * 3),
            (width / 5 * 4, height / 5 * 4),
            (width / 5 * 2, height / 5 * 2),
            (width / 5 * 2, height / 5 * 2.7),
            (width / 5 * 2, height / 5 * 3.3),
            (width / 5 * 2, height / 5 * 4),
        ]
        super().__init__(width, height, squad, id, sasiedzi, distance, defense)
        self.rect = self.surf.get_frect(topright=(width * 2, 0))
        self.load_defend_army()
        self.width = width

    def draw(self, screen):
        self.surf.fill("white")
        for pozycja in self.pozycje_group:
            pozycja.display(self.surf, self.squad.color)
        if self.squad.wzmocnienie:
            text = AssetManager.get_font("consolas", 20).render(
                f"obrona: {self.defense*100 + 5}%", True, "black"
            )
        else:
            text = AssetManager.get_font("consolas", 20).render(
                f"obrona: {self.defense*100}%", True, "black"
            )
        text_rect = text.get_frect(topright=(self.width - 100, 50))
        self.surf.blit(text, text_rect)
        screen.blit(self.surf, self.rect)

    def update_atak_points(self):
        for pozycja in self.pozycje_group:
            if pozycja.wojownik is not None:
                pozycja.wojownik.atak_points = pozycja.wojownik.jednostka["atak_points"]
