import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird AI Control")

# Load assets
bird_image = pygame.image.load("resources/bird.png")
bird_image = pygame.transform.scale(bird_image, (50, 35))

pipe_top = pygame.image.load("resources/pipe.jpg")
pipe_top = pygame.transform.scale(pipe_top, (80, 400))
pipe_bottom = pygame.transform.flip(pipe_top, False, True)

# Colors
WHITE = (255, 255, 255)

# Game Variables
gravity = 0.4
bird_x, bird_y = 100, HEIGHT // 2
bird_velocity = 0
jump_strength = -8  # Upward movement on jump
pipe_speed = 3
score = 0
pipes = []

# Add pipes
def create_pipe():
    gap = 150  # Space between top and bottom pipes
    top_pipe_height = random.randint(150, 400)
    bottom_pipe_y = top_pipe_height + gap
    pipes.append({"x": WIDTH, "top": top_pipe_height, "bottom": bottom_pipe_y})

# Game loop
running = True
clock = pygame.time.Clock()

# Create initial pipes
create_pipe()

while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Space bar makes the bird jump
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = jump_strength  # Move bird up

    # Bird physics
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pipe movement
    for pipe in pipes:
        pipe["x"] -= pipe_speed

    # Remove off-screen pipes and generate new ones
    if pipes[0]["x"] < -80:
        pipes.pop(0)
        create_pipe()
        score += 1  # Increase score when passing pipes

    # Collision detection
    for pipe in pipes:
        if (
            bird_x < pipe["x"] + 80
            and bird_x + 50 > pipe["x"]
            and (bird_y < pipe["top"] or bird_y + 35 > pipe["bottom"])
        ):
            print("Game Over!")
            bird_y = HEIGHT // 2  # Reset bird
            pipes.clear()  # Clear pipes
            create_pipe()  # Add new pipes
            score = 0  # Reset score
            bird_velocity = 0  # Reset movement

    # Check if bird hits the ground
    if bird_y > HEIGHT - 50 or bird_y < 0:
        print("Game Over!")
        bird_y = HEIGHT // 2
        pipes.clear()
        create_pipe()
        score = 0
        bird_velocity = 0

    # Draw pipes
    for pipe in pipes:
        screen.blit(pipe_top, (pipe["x"], pipe["top"] - 400))  # Top pipe
        screen.blit(pipe_bottom, (pipe["x"], pipe["bottom"]))  # Bottom pipe

    # Draw bird
    screen.blit(bird_image, (bird_x, bird_y))

    # Draw score
    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)  # 30 FPS

pygame.quit()
