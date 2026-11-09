import pygame
import constants

class PlayerInfo():
    HEALTH_BAR_WIDTH = 400
    def __init__(self, health, screen):
        self.health = health
        self.max_health = health
        self.screen = screen
        self.image = pygame.Surface((self.HEALTH_BAR_WIDTH, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, "slategray3", (0, 0, self.HEALTH_BAR_WIDTH, 30))
        self.draw_health_bar()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text = self.font.render(str(self.health), True, "white")
        self.rect = self.image.get_rect()

    def draw_health_bar(self):
        pygame.draw.rect(self.image, "black", (5, 5, self.HEALTH_BAR_WIDTH - 10, 20))
        pygame.draw.rect(self.image, "red", (5, 5, (self.HEALTH_BAR_WIDTH-10) * (self.health/self.max_health), 20))

    def update(self, health):
        self.health = max(0, health)
        self.text = self.font.render(str(self.health), True, "white")
        self.draw_health_bar()

    def draw(self): 
        self.image.blit(self.text, (self.HEALTH_BAR_WIDTH/2 - self.text.get_width()/2, 5))
        self.screen.blit(self.image, ((constants.SCREEN_WIDTH/2) - (self.HEALTH_BAR_WIDTH/2) , constants.SCREEN_HEIGHT - 60))