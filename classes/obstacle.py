import random
import pygame

SPEED = 3

class Obstacle:
    def __init__(self, x: int, y: int, image : pygame.Surface, lives: int, mobile: bool, armed: bool):
        self.image = image
        self.is_transparent = False
        self.lives = lives
        self.mobile = mobile
        self.hitbox = self.image.get_rect(topleft=(x,y))

        #Concerne obstacle pouvant tirer 
        self.armed = armed
        self.shoot_cooldown = 0
        self.projectiles = []


    # Bouger l'obstacle a gauche et aleatoirement en haut ou en bas si mobile 
    def move(self):
        self.hitbox.x -= SPEED
        if self.mobile:
            self.hitbox.y += random.choice([-1, 0, 1])

    # Tirer un projectile
    def shoot(self):
        if self.armed and self.shoot_cooldown <= 0:
            projectile = pygame.Rect(self.hitbox.left - 10, self.hitbox.centery - 5, 10, 5)
            projectile_image = pygame.Surface((10, 5))
            projectile_image.fill((255, 0, 0))
            self.projectiles.append((projectile, projectile_image))
            self.shoot_cooldown = 60 

    #Faire bouger les projectiles et les supprimer s'ils sortent de l'écran
    def update_projectiles(self):
        for projectile, projectile_image in self.projectiles:
            projectile.x -= SPEED - 2
        self.projectiles = [(p, pi) for p, pi in self.projectiles if p.x > 0]

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def take_damage(self):       
        self.lives -= 1
        if self.lives <= 0:
            self.is_transparent = True

    def is_dead(self):
        return self.lives <= 0
    
    def check_collision(self, other_rect):
        return self.hitbox.colliderect(other_rect)
    
    
def spawn_obstacle(screen_width: int, screen_height: int, images: dict) -> Obstacle:
    obstacle_type = random.choice(list(images.keys()))
    image = images[obstacle_type]
 
    x = screen_width + random.randint(0, 200)
    y = random.randint(50, screen_height - image.get_height() - 50)
 
    
    if obstacle_type == "avion":
        return Obstacle(x, y, image, lives=2, mobile=True, armed=True)
    else:  
        return Obstacle(x, y, image, lives=1, mobile=False, armed=False)