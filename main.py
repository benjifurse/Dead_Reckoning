import pygame
from tank import Tank
import constants
import math
from damage_text import DamageText
from player_info import PlayerInfo
import pytmx
import pyscroll

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dead Reckoning")

#Load the tiled map
tmx = pytmx.load_pygame("Maps/Test.tmx")
map_data = pyscroll.data.TiledMapData(tmx)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
map_layer.zoom = constants.ZOOM
background_group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=10)

#tank movement variables
turning_left = False
turning_right = False
moving_forward = False
moving_backward = False


player_tank = Tank(100, 100, "player", screen, map_layer.translate_point)
background_group.add(player_tank, layer=10) 
background_group.add(player_tank.tank_turret, layer=11)
enemy_tanks = pygame.sprite.Group()
enemy_tank = Tank(300, 600, "enemy", screen, map_layer.translate_point)
enemy_tanks.add(enemy_tank)
all_tanks = pygame.sprite.Group(player_tank, enemy_tank)
background_group.add(enemy_tank, layer=10)
background_group.add(enemy_tank.tank_turret, layer=11)
enemy_tank.tank_turret.target = player_tank

player_info = PlayerInfo(player_tank.health, screen)

projectiles = pygame.sprite.Group()

damage_texts = pygame.sprite.Group()


clock = pygame.time.Clock()
running = True

while running == True:

    # Handle events (keyboard input, quitting, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #movement and rotation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                turning_left = True
            if event.key == pygame.K_d:
                turning_right = True
            if event.key == pygame.K_w:
                moving_forward = True
            if event.key == pygame.K_s:
                moving_backward = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                turning_left = False
            if event.key == pygame.K_d:
                turning_right = False
            if event.key == pygame.K_w:
                moving_forward = False
            if event.key == pygame.K_s:
                moving_backward = False
                
        #shooting
        if event.type == pygame.MOUSEBUTTONDOWN:
            projectile = player_tank.tank_turret.shoot()
            if projectile is not None:
                projectiles.add(projectile)
    

    #update tank movement and rotation based on current input states
    player_tank.rotate(turning_left, turning_right)
    player_tank.drive(moving_forward, moving_backward)
    background_group.center(player_tank.rect.center)
    
    for enemy_tank in enemy_tanks:
        projectile = enemy_tank.tank_turret.shoot()
        if projectile is not None:
            projectiles.add(projectile)

        dx = player_tank.x - enemy_tank.x
        dy = player_tank.y - enemy_tank.y

        target_angle = math.degrees(math.atan2(-dx, -dy))
        if enemy_tank.angle < target_angle:
            enemy_tank.rotate(True, False)
        else:
            enemy_tank.rotate(False, True)
        distance = math.hypot(dx, dy)

        if distance > 400: #distance the bot moves towards the player before stopping
            enemy_tank.drive(True, False)


    background_group.update()

    player_info.update(player_tank.health)

    #draw everything
    screen.fill("black")
    background_group.draw(screen)

    #update and draw projectile
    for projectile in list(projectiles):
        tank_hit, damage_amount = projectile.update(all_tanks)
        if tank_hit is not None:
            damage_position = map_layer.translate_point(
                (tank_hit.rect.centerx, tank_hit.rect.top - 20)
            )
            damage_text = DamageText(*damage_position, damage_amount, screen)
            damage_texts.add(damage_text)
        projectile.draw()

    damage_texts.update()
    damage_texts.draw(screen)

    player_info.draw()

    clock.tick(60)
   
    pygame.display.update()#last


pygame.quit()