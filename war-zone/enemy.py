# enemy.py

import pygame
import random
from settings import WIDTH, HEIGHT, ENEMY_SPEED, CODE_LENGTH

class Enemy:
    def __init__(self):
        self.image = pygame.image.load("resources/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(midtop=(random.randint(50, WIDTH - 50), 50))
        self.speed = ENEMY_SPEED
        self.code = self.generate_code()

    def generate_code(self):
        """Generate a random 4-letter code."""
        return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=CODE_LENGTH))

    def move(self):
        """Move the enemy slightly left and right (random AI)."""
        if random.choice([True, False]):
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self, screen, font):
        """Draw the enemy and their code."""
        screen.blit(self.image, self.rect)
        text = font.render(self.code, True, (255, 0, 0))
        screen.blit(text, (self.rect.centerx - 20, self.rect.y + 80))
