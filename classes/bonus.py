class Bonus:
    def __init__(self, x, y, image, bonus_type):
        self.x = x
        self.y = y
        self.image = image
        self.bonus_type = bonus_type
        self.rect = self.image.get_rect(topleft=(x, y))

    def apply(self, player):
        player.current_bonus = self.bonus_type

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
