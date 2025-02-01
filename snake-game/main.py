import pygame
import time
from pygame.locals import *
import random

SIZE = 40  # Grid size

class Food: 
    def __init__(self, parent_screen):
        self.food = pygame.image.load("resources/meat.webp").convert_alpha()
        self.food = pygame.transform.scale(self.food, (SIZE, SIZE))
        self.parent_screen = parent_screen
        self.move()  # Initialize at a valid position
    
    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))  

    def move(self):
        # Ensure food aligns with the grid and stays inside the screen bounds
        self.x = random.randint(0, (500 // SIZE) - 1) * SIZE
        self.y = random.randint(0, (500 // SIZE) - 1) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.block_x = [SIZE] * length  # Correct initial positions
        self.block_y = [SIZE] * length
        self.direction = "down"
    
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))

    def move_up(self):
        if self.direction != "down":  # Prevent reversing into itself
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)  # Temporary placeholder
        self.block_y.append(-1)

    def walk(self):
        # Move the body before updating the head
        for i in range(self.length - 1, 0, -1):
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]

        # Move the head
        if self.direction == "down":
            self.block_y[0] += SIZE
        if self.direction == "up":
            self.block_y[0] -= SIZE
        if self.direction == "left":
            self.block_x[0] -= SIZE
        if self.direction == "right":
            self.block_x[0] += SIZE

class Game: 
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((500, 500))
        self.surface.fill((255, 255, 255))
        pygame.display.set_caption("Snake Game")
        
        self.snake = Snake(self.surface, 2)
        self.food = Food(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2  # Ensure exact position match

    def play(self):
        self.snake.walk()
        self.snake.draw()  
        self.food.draw()
        self.display_score()
        pygame.display.flip()  # Update the screen after everything is drawn

        # Collision detection for snake eating food
        if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.food.x, self.food.y):
            print("Food eaten!")
            self.snake.increase_length()
            self.food.move()

        # Collision detection for snake hitting itself
        for i in range(3, self.snake.length):  # Start checking from index 3
            if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                raise Exception("Game Over")  # Raise exception to handle game over

    def show_game_over(self):
        self.surface.fill((255, 255, 255))
        font = pygame.font.SysFont('arial', 30)

        line1 = font.render(f"Game Over! Your Score: {self.snake.length}", True, (255, 0, 0))
        self.surface.blit(line1, (120, 200))

        line2 = font.render("Press ENTER to Play Again or ESC to Exit", True, (0, 0, 255))
        self.surface.blit(line2, (80, 250))

        pygame.display.flip()  # Ensure screen updates to show game over message

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:  # Restart game on ENTER
                        self.__init__()  # Re-initialize game
                        self.run()
                        waiting = False
                    elif event.key == K_ESCAPE:  # Exit game on ESC
                        pygame.quit()
                        exit()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (10, 10))

    def run(self): 
        running = True
        while running: 
            self.surface.fill((110, 110, 5))  # Clear screen ONCE per frame

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                elif event.type == QUIT: 
                    running = False 

            try:
                self.play()
                pygame.display.flip()
                time.sleep(0.2)  # Adjust speed
            except Exception:
                self.show_game_over()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
