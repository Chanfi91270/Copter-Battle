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
        self.shield_visual_until = 0
        self.bonus_key_was_pressed = False
        self.pending_bonus = None

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
        bonus_pressed = keys[self.touches["bonus"]]
        if bonus_pressed and not self.bonus_key_was_pressed and (self.bonus_bombes or self.bonus_rafale or self.bonus_shield):
            if self.bonus_bombes:
                self.bonus_bombes = False
                self.pending_bonus = "bombe"
            elif self.bonus_rafale :
                self.bonus_rafale = False
                self.pending_bonus = "rafale"
            elif self.bonus_shield:
                self.bonus_shield = False
                self.pending_bonus = "bouclier"
        self.bonus_key_was_pressed = bonus_pressed

    def move_reseau(self, touches: dict, screen_width: int, screen_height: int):
        if self.is_transparent and pygame.time.get_ticks() >= self.transparent_until:
            self.set_transparency(False)

        if self.rect.left > 0: self.rect.x -= 1
        if touches.get("gauche") and self.rect.left > 0: self.rect.x -= SPEED
        if touches.get("droite") and self.rect.right < screen_width: self.rect.x += SPEED
        if touches.get("haut") and self.rect.top > 0: self.rect.y -= SPEED
        if touches.get("bas") and self.rect.bottom < screen_height: self.rect.y += SPEED

        bonus_pressed = touches.get("bonus", False)
        if bonus_pressed and not self.bonus_key_was_pressed and (self.bonus_bombes or self.bonus_rafale or self.bonus_shield):
            if self.bonus_bombes:
                self.bonus_bombes = False
                self.pending_bonus = "bombe"
            elif self.bonus_rafale:
                self.bonus_rafale = False
                self.pending_bonus = "rafale"
            elif self.bonus_shield:
                self.bonus_shield = False
                self.pending_bonus = "bouclier"
        self.bonus_key_was_pressed = bonus_pressed

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
        self.lives -= 1
        self.set_transparency(True)
        self.transparent_until = pygame.time.get_ticks() + self.temps_bouclier 

    def consume_pending_bonus(self):
        bonus = self.pending_bonus
        self.pending_bonus = None
        return bonus

    def activate_shield_visual(self):
        self.shield_visual_until = pygame.time.get_ticks() + self.temps_bouclier

    def shield_visual_active(self):
        return pygame.time.get_ticks() < self.shield_visual_until

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)