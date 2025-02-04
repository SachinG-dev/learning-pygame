# missile.py

import pygame
from settings import MISSILE_SPEED

class Missile:
    def __init__(self, x, y, direction):
        self.image = pygame.image.load("resources/missile.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = MISSILE_SPEED * direction  # 1 = player missile, -1 = enemy missile

    def move(self):
        """Move missile up or down."""
        self.rect.y -= self.speed

    def draw(self, screen):
        """Draw the missile."""
        screen.blit(self.image, self.rect)
