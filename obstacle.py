import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.mask = pygame.mask.Mask(self.rect.size, fill=True)