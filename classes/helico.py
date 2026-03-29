import pygame


SPEED = 5

class Helicopter:
    def __init__(self, x: int, y: int, is_transparent: bool, lives: int, image : pygame.Surface, touches : dict):
        self.image = image
        self.is_transparent = is_transparent
        self.lives = lives
        self.rect = self.image.get_rect(topleft=(x, y))
        self.touches = touches
        self.transparent_until = 0

        self.bonus_shield = False
        self.bonus_bombes = False
        self.bonus_rafale = False

        self.nb_rafale = 2
        self.temps_bouclier = 2000

    def move(self, screen_width, screen_height):
        if self.is_transparent and pygame.time.get_ticks() >= self.transparent_until:
            self.set_transparency(False)

        if self.rect.left > 0: self.rect.x -= 1
        keys = pygame.key.get_pressed()
        if keys[self.touches["gauche"]] and self.rect.left > 0: self.rect.x -= SPEED
        if keys[self.touches["droite"]] and self.rect.right < screen_width: self.rect.x += SPEED
        if keys[self.touches["haut"]] and self.rect.top > 0: self.rect.y -= SPEED
        if keys[self.touches["bas"]] and self.rect.bottom < screen_height: self.rect.y += SPEED
        if keys[self.touches["bonus"]]: pass

    def toggle_shield(self):
        self.bonus_shield = not self.bonus_shield

    def set_transparency(self, is_transparent: bool):
        self.is_transparent = is_transparent
        if self.is_transparent:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)
            

    def take_damage(self):
        if self.is_transparent:
            return

        if self.bonus_shield:
            self.toggle_shield()
        else:
            self.lives -= 1
            self.set_transparency(True)
            self.transparent_until = pygame.time.get_ticks() + self.temps_bouclier 

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
