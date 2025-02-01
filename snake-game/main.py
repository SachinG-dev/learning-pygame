import pygame
import time
from pygame.locals import *
import random

SIZE = 40

class Food: 
    def __init__(self, parent_screen):
        self.food = pygame.image.load("resources/meat.webp").convert_alpha()
        self.food = pygame.transform.scale(self.food, (SIZE, SIZE))
        self.parent_screen = parent_screen
        self.x = SIZE * 2
        self.y = SIZE * 2
    
    def draw(self):
        self.parent_screen.blit(self.food, (self.x, self.y))  # Do not clear screen here

    def move(self):
        self.x = random.randint(0, (500 // SIZE) - 1) * SIZE
        self.y = random.randint(0, (500 // SIZE) - 1) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.png").convert_alpha()
        self.block = pygame.transform.scale(self.block, (SIZE, SIZE))
        self.block_x = [SIZE] * length
        self.block_y = [SIZE] * length
        self.direction = "down"
    
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def increase_length(self):
        self.length += 1
        self.block_x.append(-1)
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
        rect1 = pygame.Rect(x1, y1, SIZE, SIZE)  # Create a rectangle for the first object
        rect2 = pygame.Rect(x2, y2, SIZE, SIZE)  # Create a rectangle for the second object
        return rect1.colliderect(rect2)
    

    def play(self):
        self.snake.walk()
        self.snake.draw()  
        self.food.draw()  # Food should be drawn before updating the screen
        self.display_score()
        pygame.display.flip()  # Draw food

        
        if self.is_collision( self.snake.block_x[0],self.snake.block_y[0], self.food.x , self.food.y):
            # self.snake.length +=1
            self.snake.increase_length()
            self.food.move()
            
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score : {self.snake.length}", True, (255,255,255))
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

            
            self.play()
            pygame.display.flip()
            time.sleep(0.2)  # Adjust speed


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
