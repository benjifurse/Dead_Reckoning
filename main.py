import pygame
from tank import Tank
import constants
from random import randint
import math

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dead Reckoning")

#tank movement variables
turning_left = False
turning_right = False
moving_forward = False
moving_backward = False


player_tank = Tank(100, 100, "player", screen)
enemy_tanks = []
enemy_tank = Tank(300, 300, "enemy", screen)
enemy_tanks.append(enemy_tank)
enemy_tank.tank_turret.target = player_tank
enemy_tank = Tank(300, 500, "enemy", screen)
enemy_tanks.append(enemy_tank)
enemy_tank.tank_turret.target = player_tank


projectiles = []

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
            if projectile != None:
                projectiles.append(projectile)

    #update tank movement and rotation based on current input states
    player_tank.rotate(turning_left, turning_right)
    player_tank.drive(moving_forward, moving_backward)
    player_tank.update()
    
    for enemy_tank in enemy_tanks:
        projectile = enemy_tank.tank_turret.shoot()
        if projectile != None:
            projectiles.append(projectile)

        dx = player_tank.x - enemy_tank.x
        dy = player_tank.y - enemy_tank.y

        target_angle = math.degrees(math.atan2(-dx, -dy))
        if enemy_tank.angle < target_angle:
            enemy_tank.rotate(True, False)
        else:
            enemy_tank.rotate(False, True)
        distance = math.hypot(dx, dy)

        if distance > 200:
            enemy_tank.drive(True, False)

        enemy_tank.update()

    #draw everything
    screen.fill("black")
    player_tank.draw(screen)
    for enemy_tank in enemy_tanks:
        enemy_tank.draw(screen)

    #update and draw projectile
    for projectile in projectiles[:]:
        projectile.update()
        projectile.draw()
        #check if projectile has gone off the screen
        if projectile.rect.x < 0 or projectile.rect.x > constants.SCREEN_WIDTH or projectile.rect.y < 0 or projectile.rect.y > constants.SCREEN_HEIGHT:
            projectiles.remove(projectile)
    clock.tick(60)
   
    pygame.display.update()#last


pygame.quit()