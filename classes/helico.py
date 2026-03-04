import pygame

class Helicopter:
    def __init__(self, x: int, y: int, has_shield: bool, is_transparent: bool, lives: int):
        self.x = x
        self.y = y
        self.has_shield = has_shield
        self.is_transparent = is_transparent
        self.lives = lives

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.x -= 5
        if keys[pygame.K_RIGHT]: self.x += 5
        if keys[pygame.K_UP]: self.y -= 5
        if keys[pygame.K_DOWN]: self.y += 5

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
