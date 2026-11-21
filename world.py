import pygame
import pytmx
from obstacle import Obstacle
from tank import Tank

class World():
    def __init__(self, tmx_file, screen, camera):
        self.tmx_data = pytmx.load_pygame(tmx_file)
        self.screen = screen
        self.camera = camera
        self.obstacles = pygame.sprite.Group()
        self._load_obstacles()
        self.enemies = pygame.sprite.Group()
        self._load_enemies()


    def _load_obstacles(self):
        obstacle_layer = self.tmx_data.get_layer_by_name("Obstacles")
        for column, row, tile_gid in obstacle_layer:
            if tile_gid > 0:
                x = column * self.tmx_data.tilewidth
                y = row * self.tmx_data.tileheight
                tile_rect = (x, y, self.tmx_data.tilewidth, self.tmx_data.tileheight)
                self.obstacles.add(Obstacle(tile_rect))

    def _load_enemies(self):
        enemy_layer = self.tmx_data.get_layer_by_name("Enemies")
        for column, row, tile_gid in enemy_layer:
            if tile_gid > 0:
                x = column * self.tmx_data.tilewidth
                y = row * self.tmx_data.tileheight
                # Here you would create and add your enemy tank to a group
                # For example: self.enemies.add(EnemyTank(x, y))
                self.enemies.add(Tank(x, y, "enemy", self.screen, camera=self.camera))