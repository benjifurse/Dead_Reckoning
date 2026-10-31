import math
import pygame
from tank_turret import TankTurret
from pygame.colordict import THECOLORS
print(sorted(THECOLORS))
from random import randint
colours = [["forestgreen", "darkgreen"], ["steelblue3", "steelblue4"], ["slategray3", "slategray4"], ["tan3", "tan4"], ["aquamarine3", "aquamarine4"], ["darkolivegreen3", "darkolivegreen4"], ["red3", "red4"], ["mistyrose3", "mistyrose4"], ["bisque2", "bisque3"], ["grey20", "grey10"]]
TANK_TYPES = {
    "player" : {"health": 100, "speed":5, "colour1": colours[0][0], "colour2": colours[0][1]},
    "enemy" : {"health": 50, "speed":5, "colour1": colours[1][0], "colour2": colours[1][1]}
}
class Tank():
    ANGLE_CHANGE = 2

    def __init__(self, x, y, tank_type, screen):
        self.angle = 0
        properties = TANK_TYPES[tank_type]
        self.type = tank_type
        self.health = properties["health"]
        self.speed = properties["speed"]
        self.tank_body = pygame.Surface((50, 80), pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.tank_body, properties["colour1"], (0, 0, 50, 80))
        pygame.draw.rect(self.tank_body, properties["colour2"], (15, 0, 20, 25))
        self.tank_turret = TankTurret(self, properties["colour2"], screen)
        self.rect.center = (x, y)
        
        # Float position so small angled steps aren't lost to rect's int rounding
        self.x = float(x)
        self.y = float(y)

        self.rotated_body = self.tank_body

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
        self.rotated_body = pygame.transform.rotate(self.tank_body, self.angle)
        self.rect = self.rotated_body.get_rect(center=(round(self.x), round(self.y)))

    def update(self):
        self.tank_turret.update()

    def draw(self, display): 
        display.blit(self.rotated_body, self.rect)
        self.tank_turret.draw()