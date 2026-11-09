import pygame
import math
from projectile import Projectile
import constants
from random import randint

class TankTurret(pygame.sprite.Sprite):
    BARREL_LENGTH = 35
    TURRET_REAR_OFFSET = 5
    def __init__(self, tank, image_path, cooldown, screen, world_to_screen=None, image_pivot=None):
        super().__init__()
        self.screen = screen
        self.world_to_screen = world_to_screen
        self.tank = tank
        self.angle = 0
        self.cooldown = cooldown
        self.turret_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.turret_image
        if image_pivot is None:
            image_pivot = self.original_image.get_rect().center
        self.image_pivot = pygame.Vector2(image_pivot)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.last_fired = pygame.time.get_ticks() #exact time the last shot was fired
        self.aim_offset_x = randint(-50, 50)
        self.aim_offset_y = randint(-50, 50)

    def update(self):
        center = self._turret_center()
        if self.tank.type == "player":
            pos = pygame.mouse.get_pos()
            if self.world_to_screen is None:
                center = self.screen.get_rect().center
            else:
                center = self.world_to_screen(center)
        else:
            pos = (self.target.x + self.aim_offset_x, self.target.y + self.aim_offset_y)
        x_dist = pos[0] - center[0]
        y_dist = pos[1] - center[1]
        self.angle = math.degrees(math.atan2(-x_dist, -y_dist))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self._position_image_at_pivot(self._turret_center())

    def _position_image_at_pivot(self, world_pivot):
        image_center = pygame.Vector2(self.original_image.get_rect().center)
        pivot_offset = self.image_pivot - image_center
        radians = math.radians(self.angle)
        rotated_offset = pygame.Vector2(
            math.cos(radians) * pivot_offset.x + math.sin(radians) * pivot_offset.y,
            -math.sin(radians) * pivot_offset.x + math.cos(radians) * pivot_offset.y,
        )
        self.rect = self.image.get_rect()
        self.rect.center = pygame.Vector2(world_pivot) - rotated_offset

    # work out the center of the turret based on the tank's position and angle
    # and using an offset
    def _turret_center(self):
        body_angle = math.radians(self.tank.angle)
        return (
            self.tank.rect.centerx - math.sin(body_angle) * self.TURRET_REAR_OFFSET,
            self.tank.rect.centery - math.cos(body_angle) * self.TURRET_REAR_OFFSET,
        )
        

    def shoot(self):
        projectile = None
        if pygame.time.get_ticks() - self.last_fired >= self.cooldown: 
            angle_radians = math.radians(self.angle)
            turret_center = self._turret_center()
            barrel_end_x = turret_center[0] - math.sin(angle_radians) * self.BARREL_LENGTH
            barrel_end_y = turret_center[1] - math.cos(angle_radians) * self.BARREL_LENGTH
            projectile = Projectile(
                barrel_end_x,
                barrel_end_y,
                self.angle,
                self.tank,
                self.screen,
                self.world_to_screen)
            self.last_fired = pygame.time.get_ticks()
            self.aim_offset_x = randint(-50, 50)
            self.aim_offset_y = randint(-50, 50)

        return projectile

    def draw(self):
        self.screen.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
