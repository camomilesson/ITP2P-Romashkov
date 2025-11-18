import sys
import pygame

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

# --- Player Setup ---
player_size = (50, 50)
player_pos = [600, 360]
player_speed = 5
player_rect = pygame.Rect(player_pos[0], player_pos[1], *player_size)

# --- Terrain / Obstacles ---
terrain_rects = []

def spawn_rect(x = screen.get_width() // 2, y = screen.get_height() // 2):
    rect = pygame.Rect(x, y, 200, 50)
    terrain_rects.append(rect)

spawn_rect()

# --- Main Game Loop ---
running = True
while running:
    clock.tick(FPS)  # Maintain 60 FPS

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Player Movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_s]:
        player_rect.y += player_speed
    if keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_d]:
        player_rect.x += player_speed

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