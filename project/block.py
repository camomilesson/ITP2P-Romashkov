import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed = 0):
        super().__init__()
        # Load full tile (3-part)
        img = pygame.image.load("sprites/block.png").convert_alpha()
        img_w, img_h = img.get_size()
        left_w = img_w // 3
        mid_w = img_w // 3
        right_w = img_w // 3

        # Crop slices
        left = img.subsurface((0, 0, left_w, img_h))
        middle = img.subsurface((left_w, 0, mid_w, img_h))
        right = img.subsurface((2*left_w, 0, right_w, img_h))

        # New surface
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw left
        self.image.blit(pygame.transform.scale(left, (left_w, height)), (0, 0))

        # Draw middle horizontally
        for i in range(left_w, width - right_w, mid_w):
            self.image.blit(pygame.transform.scale(middle, (mid_w, height)), (i, 0))

        # Draw right
        self.image.blit(pygame.transform.scale(right, (right_w, height)), (width - right_w, 0))
 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed