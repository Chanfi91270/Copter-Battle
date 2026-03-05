import pygame

SPEED = 5

class Obstacle:
    def __init__(self, x: int, y: int, is_transparent: bool, lives: int):
        self.x = x
        self.y = y
        self.is_transparent = is_transparent
        self.lives = lives

    def move(self):
        while self.lives > 0:
            self.x -= SPEED
            self.y -= SPEED
            self.y += SPEED

    def take_damage(self):       
        self.lives -= 1
        if self.lives <= 0:
            self.is_transparent = True
