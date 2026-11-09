import pygame
import math
import constants

class Projectile(pygame.sprite.Sprite):
    SPEED = 20 / constants.ZOOM
    def __init__(self, x, y, angle, owner, screen, world_to_screen=None):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.angle = angle
        self.owner = owner
        self.screen = screen
        self.world_to_screen = world_to_screen
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, "orange", (4, 4), 4)
        self.rect.center = (round(self.x), round(self.y))

    def update(self, enemy_tanks):
        rad = math.radians(self.angle)
        dx = -math.sin(rad) * self.SPEED
        dy = -math.cos(rad) * self.SPEED
        self.x += dx
        self.y += dy
        self.rect.center = (round(self.x), round(self.y))

        screen_position = self._screen_position()

        if not self.screen.get_rect().collidepoint(screen_position):
            self.kill()
            return None, 10

        #check if projectile has hit an enemy tank
        tank_hit = None
        damage_amount = 10
        for enemy in enemy_tanks:
            if self.rect.colliderect(enemy.rect) and self.owner != enemy:
                tank_hit = enemy
                enemy.take_damage(damage_amount)
                self.kill()
                break
        return tank_hit, damage_amount
    

    def draw(self):
        self.screen.blit(self.image, self.image.get_rect(center=self._screen_position()))

    def _screen_position(self):
        if self.world_to_screen is None:
            return self.rect.center
        return self.world_to_screen(self.rect.center)
