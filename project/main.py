import sys
import pygame

# Start Pygame
pygame.init()

# System setup
screen = pygame.display.set_mode((1280, 720))
FPS = pygame.time.Clock()
FPS.tick(60)
running = True

# Create color objects
color1 = pygame.Color(0, 0, 0)         # Black
color2 = pygame.Color(255, 255, 255)   # White
color3 = pygame.Color(128, 128, 128)   # Grey
color4 = pygame.Color(255, 0, 0)       # Red

# Create solid objects
    # Player
    # Terrain
    # Enemies

# Create background objects
    # Background
    # Textures

# Create audio objects
    # Sounds
    # Soundtrack

#Game loop
while running:

    # Handle events
    for event in pygame.event.get():

        # Quit loop on quit event
        if event.type == pygame.QUIT:
            running = False
    
    # Render new frame on display
    pygame.display.update()


# Exit game
pygame.quit()
sys.exit()