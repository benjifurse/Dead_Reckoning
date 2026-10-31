import pygame
import math

class Projectile():
    SPEED = 20
    def __init__(self, x, y, angle, screen):
        self.x = x
        self.y = y
        self.angle = angle-90 #barrel offset
        self.screen = screen
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, "orange", (4, 4), 4)
        self.rect.center = (x, y)

    def update(self):
        rad = math.radians(self.angle)
        dx = -math.sin(rad) * self.SPEED
        dy = -math.cos(rad) * self.SPEED
        
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        self.screen.blit(self.image, (self.rect.centerx, self.rect.centery))
