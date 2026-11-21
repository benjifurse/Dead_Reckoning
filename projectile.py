import pygame
import math
import constants

class Projectile(pygame.sprite.Sprite):
    SPEED = 20 / constants.ZOOM
    DAMAGE_AMOUNT = 10
    def __init__(self, x, y, angle, owner, screen, camera=None):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.owner = owner
        self.screen = screen
        self.camera = camera
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, "orange", (4, 4), 4)
        self.rect.center = (round(self.x), round(self.y))

    def update(self, enemy_tanks, obstacles):
        rad = math.radians(self.angle)
        dx = -math.sin(rad) * self.SPEED
        dy = -math.cos(rad) * self.SPEED

        self.x += dx
        self.y += dy
        self.rect.center = (round(self.x), round(self.y))

        #Check for collision with obstacles
        if obstacles is not None and pygame.sprite.spritecollideany(self, obstacles) is not None:
            self.kill()
            return None, 0

        #Check if projectile is off screen
        if not self.screen.get_rect().collidepoint(self._screen_position()):
            self.kill()
            return None, 0

        #Check if projectile has hit an enemy tank
        tank_hit = None
        for enemy in enemy_tanks:
            if self.rect.colliderect(enemy.rect) and self.owner != enemy:
                tank_hit = enemy
                enemy.take_damage(self.DAMAGE_AMOUNT)
                self.kill()
                break
        return tank_hit, self.DAMAGE_AMOUNT
    
    def draw(self):
        self.screen.blit(self.image, self.image.get_rect(center=self._screen_position()))

    def _screen_position(self):
        if self.camera is None:
            return self.rect.center
        return self.camera.translate_point(self.rect.center)
