import math
import pygame
from tank_turret import TankTurret
import constants

TANK_TYPES = {
    "player" : {"health": 100, "speed":3, "cooldown":500, 
                "body_image_name": "player_3_body_1.png", "turret_image_name": "player_3_turret.png",
                "turret_pivot": (12, 36)},
    "enemy" : {"health": 100, "speed":3, "cooldown":1000, 
               "body_image_name": "enemy_6_body_1.png", "turret_image_name": "enemy_6_turret.png",
               "turret_pivot": (11, 35)}
}
class Tank(pygame.sprite.Sprite):
    ANGLE_CHANGE = 2

    def __init__(self, x, y, tank_type, screen, camera=None):
        super().__init__()
        self.angle = 0
        properties = TANK_TYPES[tank_type]
        self.type = tank_type
        self.health = properties["health"]
        self.speed = properties["speed"] / constants.ZOOM
        self.tank_turret = TankTurret(self, f"{constants.TANK_IMAGE_PATH}{properties['turret_image_name']}",
                                         properties["cooldown"], screen, camera,
                                         properties["turret_pivot"])

        # Float position so small angled steps aren't lost to rect's int rounding
        self.x = float(x)
        self.y = float(y)

        original_image = pygame.image.load(
            f"{constants.TANK_IMAGE_PATH}{properties['body_image_name']}"
        ).convert_alpha()
        self.original_image = pygame.transform.scale_by(original_image, constants.TANK_SCALE)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.mask = pygame.mask.from_surface(self.image)

    def drive(self, forward, backward, obstacles=None):
        direction = 0
        if forward == True:
            direction += 1
        if backward == True:
            direction -= 1

        rad = math.radians(self.angle)
        dx = -math.sin(rad) * self.speed * direction
        dy = -math.cos(rad) * self.speed * direction

        previous_x = self.x
        previous_y = self.y
        self.x += dx
        self.y += dy
        self.rect.center = (round(self.x), round(self.y)) #rect position is in ints
        if self._collides_with_obstacles(obstacles):
            #Revert to previous position if colliding with an obstacle
            self.x = previous_x
            self.y = previous_y
            self.rect.center = (round(self.x), round(self.y))
            return False
        return True


    def rotate(self, left, right, obstacles):
        angle = self.angle
        if left == True:
            angle += self.ANGLE_CHANGE
        if right == True:
            angle -= self.ANGLE_CHANGE

        image = pygame.transform.rotate(self.original_image, angle)
        previous_rect = self.rect
        previous_mask = self.mask
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.mask = pygame.mask.from_surface(image)

        if self._collides_with_obstacles(obstacles):
            #Revert to previous angle if colliding with an obstacle
            self.rect = previous_rect
            self.mask = previous_mask
            return False
        self.angle = angle
        self.image = image
        return True

    def _collides_with_obstacles(self, obstacles):
        return obstacles is not None and pygame.sprite.spritecollideany(self, obstacles, pygame.sprite.collide_mask) is not None

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.type} damage_taken={amount}, health={self.health}")
        if self.health <= 0:
            self.tank_turret.kill()
            self.kill()

