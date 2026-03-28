import pygame
import random

BONUS_SPEED = 3


class Bonus:
    def __init__(self, x: int, y: int, image: pygame.Surface, bonus_type: str, duration: int = 300):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = True

        self.bonus_type = bonus_type
        self.duration = duration

    def move(self):
        self.rect.x -= BONUS_SPEED

    def apply(self, helicopter):
        if self.bonus_type == "bombe":
            helicopter.bonus_bombes = True
            helicopter.bonus_shield = False
            helicopter.bonus_rafale = False

        elif self.bonus_type == "rafale":
            helicopter.bonus_rafale = True
            helicopter.bonus_shield = False
            helicopter.bonus_bombes = False

        elif self.bonus_type == "bouclier":
            helicopter.bonus_shield = True
            helicopter.bonus_bombes = False
            helicopter.bonus_rafale = False

        self.active = False

    def check_collision(self, helicopter):
        return self.rect.colliderect(helicopter.rect)


def spawn_bonus(screen_width: int, screen_height: int, images: dict) -> Bonus:
    bonus_type = random.choice(list(images.keys()))
    image = images[bonus_type]

    x = screen_width + random.randint(0, 200)
    y = random.randint(50, screen_height - image.get_height() - 50)

    return Bonus(x, y, image, bonus_type)