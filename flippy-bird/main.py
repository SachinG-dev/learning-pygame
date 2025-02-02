import pygame
import random
import cv2
import mediapipe as mp
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h  # Full-screen size
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Bird - Jump to Fly")

# Load assets
bird_image = pygame.image.load("resources/ball.webp").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (100, 100))

pipe_top = pygame.image.load("resources/pipe.png").convert_alpha()
pipe_top = pygame.transform.scale(pipe_top, (80, 400))
pipe_bottom = pygame.transform.flip(pipe_top, False, True)

# Colors
WHITE = (255, 255, 255)

# Game Variables
gravity = 0.3  
bird_x, bird_y = 100, HEIGHT // 2
bird_velocity = 0
jump_strength = -6  
pipe_speed = 2  
score = 0
pipes = []
pipe_spacing = 300  # Space between pipes

# Initialize OpenCV and Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Set webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Store previous head positions for smoothing
prev_head_positions = []
SMOOTHING_FRAMES = 5
JUMP_THRESHOLD = 15  

# Create pipes
def create_pipe():
    gap = HEIGHT // 4  
    top_pipe_height = random.randint(HEIGHT // 6, HEIGHT // 2)
    bottom_pipe_y = top_pipe_height + gap

    # Ensure bottom pipe is correctly positioned
    if bottom_pipe_y + 400 > HEIGHT:  
        bottom_pipe_y = HEIGHT - 400
    
    pipes.append({"x": WIDTH, "top": top_pipe_height, "bottom": bottom_pipe_y})

# Game loop
running = True
clock = pygame.time.Clock()
create_pipe()

while running:
    screen.fill(WHITE)

    # Capture webcam frame
    ret, frame = cap.read()
    if not ret:
        print("❌ ERROR: Webcam not working!")
        break

    # Rotate frame if it's incorrectly oriented
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  

    # Convert frame to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Draw skeleton outline on the user
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get the nose landmark (head position)
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        head_y = int(nose.y * HEIGHT)

        # Store last few head positions for smoothing
        prev_head_positions.append(head_y)
        if len(prev_head_positions) > SMOOTHING_FRAMES:
            prev_head_positions.pop(0)

        # Calculate the average head position over the last few frames
        smoothed_head_y = np.mean(prev_head_positions)

        # Compare with previous position to detect jump
        if len(prev_head_positions) >= 2:
            head_movement = prev_head_positions[-2] - smoothed_head_y  

            if head_movement > JUMP_THRESHOLD:  
                bird_velocity = jump_strength
                print("✅ Jump Detected!")

    # Flip the frame for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert OpenCV frame to Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    
    # Resize and position video feed (Top Right Corner - 300x300)
    frame = pygame.transform.scale(frame, (300, 300))
    screen.blit(frame, (WIDTH - 310, 10))  # 10px padding from the top-right

    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to exit
                running = False
            if event.key == pygame.K_SPACE:  # Press SPACE to jump
                bird_velocity = jump_strength

    # Bird physics (apply gravity)
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pipe movement
    for pipe in pipes:
        pipe["x"] -= pipe_speed

    # Remove off-screen pipes and add new ones at correct spacing
    if len(pipes) > 0 and pipes[0]["x"] < -80:
        pipes.pop(0)

    # Add new pipes only when the last pipe has moved far enough
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - pipe_spacing:
        create_pipe()
        score += 1

    # Collision detection
    for pipe in pipes:
        if (
            bird_x < pipe["x"] + 80
            and bird_x + 50 > pipe["x"]
            and (bird_y < pipe["top"] or bird_y + 35 > pipe["bottom"])
        ):
            print("Game Over!")
            bird_y = HEIGHT // 2
            pipes.clear()
            create_pipe()
            score = 0
            bird_velocity = 0

    # Check if bird hits ground
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
    clock.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
