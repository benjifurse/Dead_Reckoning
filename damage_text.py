import pygame

class DamageText(pygame.sprite.Sprite):
    LIFETIME = 1000  # milliseconds
    def __init__(self, x, y, damage, screen):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.screen = screen
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.image = self.font.render(str(damage), True, (255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = self.LIFETIME
        self.start_time = pygame.time.get_ticks()
        self.alpha = 255  # Start fully solid colour

    def update(self):
        self.rect.y -= 1
        alpha_change = self.alpha/self.LIFETIME * 40
        self.alpha = max(0, self.alpha - alpha_change)  # Fade out over time, max ensures it doesnt go below 0
        self.image.set_alpha(self.alpha)
        if pygame.time.get_ticks() - self.start_time > self.LIFETIME:
            self.kill()