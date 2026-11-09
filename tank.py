import math
import pygame
from tank_turret import TankTurret
import constants

TANK_TYPES = {
    "player" : {"health": 100, "speed":5, "cooldown":500, 
                "body_image_name": "player_3_body_1.png", "turret_image_name": "player_3_turret.png",
                "turret_pivot": (12, 36)},
    "enemy" : {"health": 100, "speed":5, "cooldown":1000, 
               "body_image_name": "enemy_6_body_1.png", "turret_image_name": "enemy_6_turret.png",
               "turret_pivot": (11, 35)}
}
class Tank(pygame.sprite.Sprite):
    ANGLE_CHANGE = 2

    def __init__(self, x, y, tank_type, screen, world_to_screen=None):
        super().__init__()
        self.angle = 0
        properties = TANK_TYPES[tank_type]
        self.type = tank_type
        self.health = properties["health"]
        self.speed = properties["speed"] / constants.ZOOM
        #self.tank_body = pygame.Surface((50, 80), pygame.SRCALPHA)
        #self.rect = pygame.draw.rect(self.tank_body, properties["colour1"], (0, 0, 50, 80))
        #pygame.draw.rect(self.tank_body, properties["colour2"], (15, 0, 20, 25))
        self.tank_turret = TankTurret(self, f"{constants.TANK_IMAGE_PATH}{properties['turret_image_name']}",
                                         properties["cooldown"], screen, world_to_screen,
                                         properties["turret_pivot"])
        #self.rect.center = (x, y)
        
        # Float position so small angled steps aren't lost to rect's int rounding
        self.x = float(x)
        self.y = float(y)

        self.original_image = pygame.image.load(
            f"{constants.TANK_IMAGE_PATH}{properties['body_image_name']}"
        ).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))

    def drive(self, forward, backward):
        direction = 0
        if forward == True:
            direction += 1
        if backward == True:
            direction -= 1

        rad = math.radians(self.angle)
        dx = -math.sin(rad) * self.speed * direction
        dy = -math.cos(rad) * self.speed * direction

        self.x += dx
        self.y += dy
        self.rect.center = (round(self.x), round(self.y)) #rect position is in ints

    def rotate(self, left, right):

        if left == True:
            self.angle += self.ANGLE_CHANGE
        if right == True:
            self.angle -= self.ANGLE_CHANGE

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.type} damage_taken={amount}, health={self.health}")
        if self.health <= 0:
            self.tank_turret.kill()
            self.kill()

