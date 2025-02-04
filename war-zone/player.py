# player.py

import pygame
import random
from settings import WIDTH, HEIGHT, PLAYER_SPEED, CODE_LENGTH

class Player:
    def __init__(self):
        self.image = pygame.image.load("resources/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        self.code = self.generate_code()
        self.speed = PLAYER_SPEED

    def generate_code(self):
        """Generate a random 4-letter code."""
        return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=CODE_LENGTH))

    def move(self, keys):
        """Handles player movement using arrow keys."""
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen, font):
        """Draws the player and their code."""
        screen.blit(self.image, self.rect)
        text = font.render(self.code, True, (0, 255, 0))
        screen.blit(text, (self.rect.centerx - 20, self.rect.y - 30))
