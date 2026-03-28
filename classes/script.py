import pygame
from classes.helico import Helicopter
from classes.obstacle import Obstacle, spawn_obstacle
from classes.bonus import Bonus, spawn_bonus
from classes.joueur import Joueur  
 

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Copter Battle")
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

#Images pour fond

image_fond_menu = pygame.image.load('./images/fond_accueil.png').convert()
image_fond_menu = pygame.transform.scale(image_fond_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

image_desert = pygame.image.load('./images/fond_jeu.png').convert()
image_desert = pygame.transform.scale(image_desert, (SCREEN_WIDTH, SCREEN_HEIGHT))

img_helico1 = pygame.image.load('./images/helicoJ1.png').convert_alpha()
img_helico1 = pygame.transform.scale(img_helico1, (210, 180))

img_helico2 = pygame.image.load('./images/helicoJ2.png').convert_alpha()
img_helico2 = pygame.transform.scale(img_helico2, (210, 180))

gif_chargement = []
for i in range(1, 9):  # 8 frames
    img = pygame.image.load(f'./images/gif/loading_{i}.png').convert_alpha()
    gif_chargement.append(img)

touches_j1 = {"gauche": pygame.K_q, "droite": pygame.K_d, "haut": pygame.K_z, "bas": pygame.K_s, "bonus": pygame.K_a}
touches_j2 = {"gauche": pygame.K_LEFT, "droite": pygame.K_RIGHT, "haut": pygame.K_UP, "bas": pygame.K_DOWN, "bonus": pygame.K_RSHIFT}

helico1 = Helicopter(50, 100, False, False,3,img_helico1, touches_j1)
helico2 = Helicopter(50, SCREEN_HEIGHT - 250, False, False, 3,img_helico2, touches_j2)

#Images pour obstacles
img_rock = pygame.image.load('./images/rock.png').convert_alpha()
img_avion = pygame.image.load('./images/avion.png').convert_alpha()
img_avion = pygame.transform.scale(img_avion, (100, 100))

images_obstacles = {
    "rock": img_rock,
    "avion": img_avion
}

obstacles = []
spawn_timer = 0


img_bonus_bombe = pygame.image.load('./images/bombe.png').convert_alpha()
img_bonus_rafale = pygame.image.load('./images/rafale_tir.png').convert_alpha()
img_bonus_bouclier = pygame.image.load('./images/bouclier.png').convert_alpha()

images_bonus = {
    "bombe": img_bonus_bombe,
    "rafale": img_bonus_rafale,
    "bouclier": img_bonus_bouclier
}

bonuses = []
bonus_spawn_timer = 0


Vert = (120, 150, 80)
Blanc = (255, 255, 255)
Noir = (0, 0, 0)
Gris = (200, 200, 200)
Gris_fonce = (100, 100, 100)

font_titre = pygame.font.SysFont("Impact", 150)
font_menu = pygame.font.SysFont("Arial", 30, bold=True)
font_sub = pygame.font.SysFont("Arial", 25, bold=False)

bouton_lancer = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 220, 70)
bouton_rejoindre = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50, 220, 70)

h1_x, h1_y = 50, 100
h2_x, h2_y = 50, SCREEN_HEIGHT - 250

etape = "ACCUEIL"

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if etape == "ACCUEIL" and event.key == pygame.K_SPACE:
                etape = "MENU_CHOIX"
            elif etape == "ATTENTE_J2" and event.key == pygame.K_SPACE:
                etape = "EN_JEU"

        if etape == "MENU_CHOIX" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_lancer.collidepoint(mouse_pos):
                etape = "ATTENTE_J2"
            elif bouton_rejoindre.collidepoint(mouse_pos):
                etape = "ATTENTE"

    # --- PARTIE DESSIN PAR ETAPE ---

    if etape == "ACCUEIL":
        screen.blit(image_fond_menu, (0, 0))  # Fond ici
        txt_titre = font_titre.render("COPTER BATTLE", True, Vert)
        screen.blit(txt_titre, txt_titre.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
        txt_msg = font_menu.render("APPUYEZ SUR ESPACE POUR COMMENCER", True, Blanc)
        screen.blit(txt_msg, txt_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

    elif etape == "MENU_CHOIX":
        screen.blit(image_fond_menu, (0, 0))  # Fond ici aussi
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        if bouton_lancer.collidepoint(mouse_pos):
            c_lancer = Gris_fonce
        else:
            c_lancer = Gris
        pygame.draw.rect(screen, c_lancer, bouton_lancer, border_radius=10)
        t_lancer = font_menu.render("LANCER", True, Noir)
        screen.blit(t_lancer, t_lancer.get_rect(center=bouton_lancer.center))

        if bouton_rejoindre.collidepoint(mouse_pos):
            c_rejoindre = Gris_fonce
        else:
            c_rejoindre = Gris
        pygame.draw.rect(screen, c_rejoindre, bouton_rejoindre, border_radius=10)
        t_rejoindre = font_menu.render("REJOINDRE", True, Noir)
        screen.blit(t_rejoindre, t_rejoindre.get_rect(center=bouton_rejoindre.center))

    elif etape == "ATTENTE_J2":
        screen.blit(image_desert, (0, 0))  # Fond desert ici
        screen.blit(img_helico1, (h1_x, h1_y))
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        txt_attente = font_menu.render("EN ATTENTE JOUEUR 2", True, Blanc)
        txt_action = font_sub.render("appuyer sur espace pour rejoindre", True, Gris)
        screen.blit(txt_attente, txt_attente.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(txt_action, txt_action.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))

    elif etape == "ATTENTE":
        screen.blit(image_desert, (0, 0))  # Fond desert ici
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        txt_wait = font_menu.render("RECHERCHE D'UN ADVERSAIRE...", True, Blanc)
        screen.blit(txt_wait, txt_wait.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))


    elif etape == "EN_JEU":
        screen.blit(image_desert, (0, 0))

        # Spawn aléatoire
        spawn_timer += 1
        if spawn_timer >= 120:  # toutes les 2 secondes environ
            obstacles.append(spawn_obstacle(SCREEN_WIDTH, SCREEN_HEIGHT, images_obstacles))
            spawn_timer = 0

        bonus_spawn_timer += 1
        if bonus_spawn_timer >= 180:  # toutes les 3 secondes environ
            bonuses.append(spawn_bonus(SCREEN_WIDTH, SCREEN_HEIGHT, images_bonus))
            bonus_spawn_timer = 0

        # Mettre à jour et dessiner les obstacles
        for obs in obstacles:
            obs.move()
            obs.shoot()
            obs.update_projectiles()
            screen.blit(obs.image, obs.hitbox)
            if obs.check_collision(helico1):
              helico1.take_damage()
              obs.take_damage()
            if obs.check_collision(helico2):
              helico2.take_damage()
              obs.take_damage()

         # Mettre à jour et dessiner les bonus
        for bonus in bonuses:
         bonus.move()
         screen.blit(bonus.image, bonus.rect)

         if bonus.check_collision(helico1):
            bonus.apply(helico1)

         elif bonus.check_collision(helico2):
            bonus.apply(helico2)

        # Supprimer les obstacles hors écran
        obstacles = [o for o in obstacles if not o.hitbox.right < 0 and not o.is_dead()]

        # Supprimer les bonus hors écran
        bonuses = [b for b in bonuses if not b.rect.right < 0 and b.active]

        # Hélicos
        helico1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
        helico2.move(SCREEN_WIDTH, SCREEN_HEIGHT)
        screen.blit(helico1.image, helico1.rect)
        screen.blit(helico2.image, helico2.rect)
        if helico1.check_collision(helico2):
           helico2.image.set_alpha(128)
        else:
           helico2.image.set_alpha(255)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
