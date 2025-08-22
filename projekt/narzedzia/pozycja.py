import pygame
from projekt.narzedzia import calc_scaled_offset
from projekt.assetMenager import AssetManager


class Pozycja(pygame.sprite.Sprite):
    def __init__(self, offset, start, width, height, group, skala, id):
        super().__init__(group)
        self.surf = pygame.Surface((width, height))
        self.color = "white"
        self.surf.fill(self.color)
        self.pos = calc_scaled_offset(offset, start, skala * 1.5)
        self.rect = self.surf.get_frect(center=self.pos)
        self.wojownik = None
        self.id = id
        self.healthbar = pygame.Surface((10, 60))
        self.healthbar.fill("white")
        self.healthbar_rect = self.healthbar.get_frect(
            center=(self.pos[0] - 45, self.pos[1])
        )

    def hover(self, mouse_pos):
        if self.color == (200, 200, 200):
            return
        if self.rect.collidepoint(mouse_pos):
            self.color = (220, 220, 220)
        else:
            self.color = "white"

    def display(self, screen, color):
        self.surf.fill(self.color)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "black", self.rect, width=1)
        if self.wojownik is None:
            return
        surf = AssetManager.get_unit(self.wojownik.name, color)
        rect = surf.get_frect(center=self.pos)
        screen.blit(surf, rect)
        self.display_health(screen)

    def display_health(self, screen):
        if self.wojownik is None:
            return
        procent = self.wojownik.zdrowie / self.wojownik.jednostka["zdrowie"]
        screen.blit(self.healthbar, self.healthbar_rect)
        if procent > 0.00001:
            health = pygame.Surface((10, 60 * procent))
            if procent < 0.25:
                health.fill("red")
            else:
                health.fill("green")
            screen.blit(
                health,
                health.get_frect(bottomleft=(self.pos[0] - 50, self.pos[1] + 30)),
            )
        pygame.draw.rect(screen, "black", self.healthbar_rect, width=1)


class AttackPosition(Pozycja):
    def __init__(self, offset, start, width, height, group, skala, id):
        super().__init__(offset, start, width, height, group, skala, id)
        self.pos = offset
        self.rect = self.surf.get_frect(center=self.pos)
        self.healthbar_rect = self.healthbar.get_frect(
            center=(self.pos[0] - 45, self.pos[1])
        )

    def display(self, screen, color):
        self.surf.fill(self.color)
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, "black", self.rect, width=1)
        if self.wojownik is None:
            return
        surf = AssetManager.get_unit(self.wojownik.name, color)
        rect = surf.get_frect(center=self.pos)
        screen.blit(surf, rect)
        self.display_health(screen)
        self.display_attacks(screen)

    def display_attacks(self, screen):
        display = str(
            int(self.wojownik.atak_points / self.wojownik.bronie[0]["koszt_ataku"])
        )
        text = AssetManager.get_font("consolas", 20).render(display, True, "black")
        text_rect = text.get_frect(center=(self.pos[0] + 30, self.pos[1] - 30))
        screen.blit(text, text_rect)
