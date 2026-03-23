import pygame

SPEED = 5

class Helicopter:
    def __init__(self, x: int, y: int, has_shield: bool, is_transparent: bool, lives: int):
        self.has_shield = has_shield
        self.is_transparent = is_transparent
        self.lives = lives
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= SPEED
        if keys[pygame.K_RIGHT]: self.rect.x += SPEED
        if keys[pygame.K_UP]: self.rect.y -= SPEED
        if keys[pygame.K_DOWN]: self.rect.y += SPEED

    def toggle_shield(self):
        self.has_shield = not self.has_shield

    def set_transparency(self, is_transparent: bool):
        self.is_transparent = is_transparent
        pygame.time.wait(3000)
        self.is_transparent = False

    def take_damage(self):
        if self.has_shield:
            self.toggle_shield()
        else:
            self.lives -= 1
            self.set_transparency(True)

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
