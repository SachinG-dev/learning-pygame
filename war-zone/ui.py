# ui.py

import pygame
from settings import WHITE

def display_score(screen, font, score):
    """Displays the player's score."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(screen, font):
    """Displays the game over screen."""
    screen.fill((0, 0, 0))
    text = font.render("GAME OVER! Press R to Restart", True, WHITE)
    screen.blit(text, (200, 300))
    pygame.display.flip()
