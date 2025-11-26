import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        image_idle = pygame.image.load("sprites/player_idle.png").convert_alpha()
        self.image_idle = pygame.transform.scale(image_idle, (40, 60))
        image_jumping = pygame.image.load("sprites/player_jumping.png").convert_alpha()
        self.image_jump = pygame.transform.scale(image_jumping, (40, 60))
        self.image = self.image_idle  # default
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0.0
        self.vel_x = 0.0