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
pygame.display.set_caption("Star Wars - Object Collection")

# Load player image (Bigger height)
player_image = pygame.image.load("resources/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (200, 180))  # Increased height

# Load falling object (Bigger size)
object_image = pygame.image.load("resources/asteroid.webp").convert_alpha()
object_image = pygame.transform.scale(object_image, (100, 100))  # Increased size

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Reference point marker color

# Game Variables
player_x = WIDTH // 2
player_y = HEIGHT - 200  # Adjusted for larger player image
player_speed = 10
falling_speed = 5
score = 0

# Initialize Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Function to list available cameras
def list_cameras():
    available_cameras = []
    for i in range(5):  # Check first 5 indices for available cameras
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:  # If camera is available, add it to list
            available_cameras.append(i)
        cap.release()
    return available_cameras

# Allow user to select a camera
available_cams = list_cameras()
if len(available_cams) > 1:
    print("\n🎥 Multiple cameras detected:")
    for cam in available_cams:
        print(f"[{cam}] Camera {cam}")
    selected_cam = int(input("Enter the camera index to use: "))
else:
    selected_cam = available_cams[0] if available_cams else 0  # Default to first available camera

# Open selected camera
cap = cv2.VideoCapture(selected_cam)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Store previous head positions for movement smoothing
prev_head_positions = []
SMOOTHING_FRAMES = 5
MOVE_THRESHOLD = 40  # Increased to prevent unnecessary movements

# Define center point for user movement tracking
CAM_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # Get actual camera width
CAM_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # Get actual camera height
CAM_CENTER = CAM_WIDTH // 2  # The center of the camera frame

# Scaling factor to map camera movements to screen
screen_scaling_factor = WIDTH / CAM_WIDTH  

# Create falling objects
objects = [{"x": random.randint(50, WIDTH - 50), "y": 0}]
def spawn_object():
    objects.append({"x": random.randint(50, WIDTH - 50), "y": 0})

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Capture webcam frame
    ret, frame = cap.read()
    if not ret:
        print("❌ ERROR: Camera not working!")
        break

    # **Fix: Correct Camera Orientation**
    frame = cv2.flip(frame, 1)  # Flip horizontally for correct mirroring
    frame = cv2.resize(frame, (640, 480))  # Ensure correct aspect ratio

    # Convert frame to RGB for Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # Draw reference point on user camera feed
    cv2.line(frame, (CAM_CENTER - MOVE_THRESHOLD, 0), (CAM_CENTER - MOVE_THRESHOLD, CAM_HEIGHT), GREEN, 2)  # Left marker
    cv2.line(frame, (CAM_CENTER + MOVE_THRESHOLD, 0), (CAM_CENTER + MOVE_THRESHOLD, CAM_HEIGHT), GREEN, 2)  # Right marker

    # Draw skeleton outline on the user
    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get nose position (user's head center)
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        head_x = int(nose.x * CAM_WIDTH)

        # Store last few head positions for smoothing
        prev_head_positions.append(head_x)
        if len(prev_head_positions) > SMOOTHING_FRAMES:
            prev_head_positions.pop(0)

        # Smooth head position
        smoothed_head_x = np.mean(prev_head_positions)

        # Move player based on center reference point
        if smoothed_head_x > CAM_CENTER + MOVE_THRESHOLD:  # Move right
            player_x += player_speed
        elif smoothed_head_x < CAM_CENTER - MOVE_THRESHOLD:  # Move left
            player_x -= player_speed

    # Keep player within screen boundaries
    player_x = max(0, min(WIDTH - player_image.get_width(), player_x))

    # Convert OpenCV frame to Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)  # **Fix: Ensure Correct Rotation**
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (350, 350))  # Increased size
    screen.blit(frame, (WIDTH - 360, 20))  # Adjusted position

    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update falling objects
    for obj in objects:
        obj["y"] += falling_speed

        # Check collision with player
        if (player_x < obj["x"] < player_x + player_image.get_width() and
                player_y < obj["y"] < player_y + player_image.get_height()):
            score += 1
            objects.remove(obj)
            spawn_object()

        # Remove objects that fall off-screen & respawn
        if obj["y"] > HEIGHT:
            objects.remove(obj)
            spawn_object()

    # Increase speed over time
    if score % 5 == 0 and score > 0:
        falling_speed += 0.05

    # Draw falling objects
    for obj in objects:
        screen.blit(object_image, (obj["x"], obj["y"]))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw score
    font = pygame.font.SysFont("Arial", 40)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(30)

cap.release()
cv2.destroyAllWindows()
pygame.quit()
