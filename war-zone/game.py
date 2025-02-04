# game.py

import pygame
import random
from player import Player
from enemy import Enemy
from missile import Missile
from ui import display_score, game_over_screen
from settings import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.player = Player()
        self.enemy = Enemy()
        self.missiles = []
        self.score = 0

    def run(self):
        """Main game loop."""
        while self.running:
            self.screen.fill((30, 30, 30))

            # Events
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart
                        self.__init__()

            # Update objects
            self.player.move(keys)
            self.enemy.move()

            for missile in self.missiles:
                missile.move()

            # Draw everything
            self.player.draw(self.screen, self.font)
            self.enemy.draw(self.screen, self.font)
            for missile in self.missiles:
                missile.draw(self.screen)

            display_score(self.screen, self.font, self.score)

            pygame.display.update()
            self.clock.tick(FPS)
