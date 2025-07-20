import pygame


class Podswietlenie(pygame.sprite.Sprite):
    def __init__(self, url, pos, group):
        super().__init__(group)
        self.image = pygame.image.load(f"Grafika/tile-grafika/efekty hexów/{url}")
        self.rect = self.image.get_frect(center=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
