import pygame
import math
from projectile import Projectile
import constants
from random import randint

class TankTurret():
    SHOT_COOLDOWN = 500 #milliseconds
    def __init__(self, tank, colour, screen):
        self.screen = screen
        self.tank = tank
        self.angle = 0
        #Create turret image
        self.turret_image = pygame.Surface((120, 80), pygame.SRCALPHA)
        self.original_image = self.turret_image
        self.rect = self.turret_image.get_rect()
        # barrel
        pygame.draw.rect(self.turret_image, colour, (50, 36, 60, 8))
        # base
        pygame.draw.circle(self.turret_image, colour, (60, 40), 15)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.last_fired = pygame.time.get_ticks() #exact time the last shot was fired
        self.aim_offset_x = randint(-50, 50)
        self.aim_offset_y = randint(-50, 50)

    def update(self):
        self.rect.center = self.tank.rect.center
        if self.tank.type == "player":
            pos = pygame.mouse.get_pos()
        else:
            pos = (self.target.x + self.aim_offset_x, self.target.y + self.aim_offset_y)
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        

    def shoot(self):
        projectile = None
        if pygame.time.get_ticks() - self.last_fired >= self.SHOT_COOLDOWN: 
            projectile = Projectile(
                self.tank.rect.centerx,
                self.tank.rect.centery,
                self.angle,
                self.screen)
            self.last_fired = pygame.time.get_ticks()
            self.aim_offset_x = randint(-50, 50)
            self.aim_offset_y = randint(-50, 50)

        return projectile

    def draw(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.screen.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
