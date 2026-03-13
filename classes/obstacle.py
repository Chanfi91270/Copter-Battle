import pygame

SPEED = 5

class Obstacle:
    def __init__(self, x: int, y: int, image : pygame.Surface, is_transparent: bool, lives: int, mobile: bool, armed: bool):
        self.x = x
        self.y = y
        self.image = image
        self.is_transparent = is_transparent
        self.lives = lives
        self.mobile = mobile
        self.armed = armed

    def move(self):
        if self.mobile:
            while self.lives > 0:
                self.x -= SPEED
                self.y -= SPEED
                self.y += SPEED

    def shoot(self):
        if self.armed:
            pass

    def take_damage(self):       
        self.lives -= 1
        if self.lives <= 0:
            self.is_transparent = True
