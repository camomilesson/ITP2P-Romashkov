import sys
import pygame
import random

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pygame HS ITP2P")
clock = pygame.time.Clock()
FPS = 60

# --- Colors ---
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREY = pygame.Color(128, 128, 128)
RED = pygame.Color(255, 0, 0)


# Player
player_size = (50, 50)
player_rect = pygame.Rect(600, 100, *player_size)
player_speed = 5
player_vel_y = 0
gravity = 0.2  # Acceleration due to gravity
max_fall_speed = 15

# --- Terrain / Obstacles ---
terrain_rects = [pygame.Rect(150, 100, 1000, 50)]
SPAWN_RECT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_RECT, 500)
terrain_speed = 2

# --- Main Game Loop ---
running = True
while running:
    clock.tick(FPS)  # Maintain 60 FPS

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_RECT:
            x = random.randint(0, 1200)  # Random x position
            y = 0                        # Spawn at top
            width = random.randint(50, 150)
            height = 50
            new_rect = pygame.Rect(x, y, width, height)
            terrain_rects.append(new_rect)

    # --- Player horizontal movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_d]:
        player_rect.x += player_speed

    # --- Gravity ---
    # Check if player is standing on any terrain
    on_ground = False
    for rect in terrain_rects:
        if player_rect.colliderect(rect) and player_rect.bottom <= rect.bottom + 10:
            # Snap player on top of rect
            player_rect.bottom = rect.top
            player_vel_y = terrain_speed
            on_ground = True
            break

    if not on_ground:
        # Apply gravity
        player_vel_y += gravity
        if player_vel_y > max_fall_speed:
            player_vel_y = max_fall_speed
        player_rect.y += int(player_vel_y)

    for rect in terrain_rects:
        rect.y += terrain_speed
        if rect.y > 3000:
            terrain_rects = [rect for rect in terrain_rects if rect.y < 720]
            break

    # --- Drawing ---
    screen.fill(BLACK)  # Clear screen

    # Draw terrain
    for rect in terrain_rects:
        pygame.draw.rect(screen, GREY, rect)

    # Draw player
    pygame.draw.rect(screen, WHITE, player_rect)

    # Update display
    pygame.display.update()

# --- Exit ---
pygame.quit()
sys.exit()