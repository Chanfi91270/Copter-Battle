import pygame
import random

SPEED = 2

class Bonus:
    def __init__(self, x, y, image, bonus_type):
        self.image = image
        self.bonus_type = bonus_type
        self.hitbox = self.image.get_rect(topleft=(x,y))
    
    def apply(self, player):
        player.current_bonus = self.bonus_type

    def move(self):
        self.hitbox.x -= SPEED
