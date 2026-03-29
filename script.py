import pygame, random
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

temps_debut_match = 0
winner_text = ""
temps_final = ""
h1_x, h1_y = 50, 100
h2_x, h2_y = 50, SCREEN_HEIGHT - 250
LIVES = 3

#Images pour fond

image_fond_menu = pygame.image.load('./images/fond_accueil.png').convert()
image_fond_menu = pygame.transform.scale(image_fond_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

image_desert = pygame.image.load('./images/fond_jeu.png').convert()
image_desert = pygame.transform.scale(image_desert, (SCREEN_WIDTH, SCREEN_HEIGHT))

image_coeur = pygame.image.load('./images/coeur.png').convert_alpha()
image_coeur = pygame.transform.scale(image_coeur, (25, 25))

image_cadre = pygame.image.load('./images/cadre.png').convert_alpha()
image_cadre = pygame.transform.scale(image_cadre, (150,100))

gif_explosion = []
for i in range(1, 6):
    img = pygame.image.load(f'./images/gif_explosion/frame_{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (110, 90))
    gif_explosion.append(img)
#Images pour hélicos

img_helico1 = pygame.image.load('./images/helicoJ1.png').convert_alpha()
img_helico1 = pygame.transform.scale(img_helico1, (110, 90))

img_helico2 = pygame.image.load('./images/helicoJ2.png').convert_alpha()
img_helico2 = pygame.transform.scale(img_helico2, (110, 90))

gif_chargement = []
for i in range(1, 9):
    img = pygame.image.load(f'./images/gif_chargement/loading_{i}.png').convert_alpha()
    gif_chargement.append(img)

touches_j1 = {"gauche": pygame.K_q, "droite": pygame.K_d, "haut": pygame.K_z, "bas": pygame.K_s, "bonus": pygame.K_a}
touches_j2 = {"gauche": pygame.K_LEFT, "droite": pygame.K_RIGHT, "haut": pygame.K_UP, "bas": pygame.K_DOWN, "bonus": pygame.K_RSHIFT}

helico1 = Helicopter(50, 100, False,LIVES,img_helico1, touches_j1)
helico2 = Helicopter(50, SCREEN_HEIGHT - 250, False, LIVES,img_helico2, touches_j2)

#Images pour obstacles
img_rock = pygame.image.load('./images/rock.png').convert_alpha()
img_rock = pygame.transform.scale(img_rock, (120, 120))
img_avion = pygame.image.load('./images/avion.png').convert_alpha()
img_avion = pygame.transform.scale(img_avion, (120, 90))

images_obstacles = {
    "rock": img_rock,
    "avion": img_avion
}

obstacles = []
spawn_timer = 0


img_bonus_bombe = pygame.image.load('./images/bombe.png').convert_alpha()
img_bonus_bombe = pygame.transform.scale(img_bonus_bombe, (60, 80))
img_bonus_rafale = pygame.image.load('./images/rafale_tir.png').convert_alpha()
img_bonus_rafale = pygame.transform.scale(img_bonus_rafale, (60, 50))
img_bonus_bouclier = pygame.image.load('./images/bouclier.png').convert_alpha()
img_bonus_bouclier = pygame.transform.scale(img_bonus_bouclier, (70, 70))

images_bonus = {
    "bombe": img_bonus_bombe,
    "rafale": img_bonus_rafale,
    "bouclier": img_bonus_bouclier
}

bonus_icons_hud = {
    "bombe": pygame.transform.smoothscale(img_bonus_bombe, (30, 30)),
    "rafale": pygame.transform.smoothscale(img_bonus_rafale, (30, 30)),
    "bouclier": pygame.transform.smoothscale(img_bonus_bouclier, (30, 30)),
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
font_bonus = pygame.font.SysFont("Arial", 18, bold=True)


def get_current_bonus(helico):
    if helico.bonus_shield:
        return "bouclier"
    if helico.bonus_rafale:
        return "rafale"
    if helico.bonus_bombes:
        return "bombe"
    return None

bouton_lancer = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 220, 70)
bouton_rejoindre = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50, 220, 70)
bouton_retour = pygame.Rect(30, SCREEN_HEIGHT - 100, 200, 70)
bouton_rejouer = pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 100, 220, 70)

explosion_start_time = None
explosion_duration_ms = 900
helico_mort = None


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
                temps_debut_match = pygame.time.get_ticks()

        # Gestion des clics Menu Choix
        if etape == "MENU_CHOIX" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_lancer.collidepoint(mouse_pos):
                etape = "ATTENTE_J2"
            elif bouton_rejoindre.collidepoint(mouse_pos):
                etape = "ATTENTE"

            # Gestion des clics pour RETOUR et REJOUER (Séparés)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # RETOUR
            if (etape == "ATTENTE_J2" or etape == "ATTENTE") and bouton_retour.collidepoint(mouse_pos):
                etape = "MENU_CHOIX"

            # REJOUER
        if etape == "GAME_OVER" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_rejouer.collidepoint(mouse_pos):
                helico1.lives = 3
                helico2.lives = 3
                # On utilise .rect.topleft pour déplacer les objets Helicopter
                helico1.rect.topleft = (50, 100)
                helico2.rect.topleft = (50, SCREEN_HEIGHT - 250)
                obstacles.clear()
                bonuses.clear()
                helico_mort = None
                explosion_start_time = None
                etape = "ATTENTE_J2"
    # --- PARTIE DESSIN PAR ETAPE ---

    if etape == "ACCUEIL":
        screen.blit(image_fond_menu, (0, 0))  
        txt_titre = font_titre.render("COPTER BATTLE", True, Vert)
        screen.blit(txt_titre, txt_titre.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
        txt_msg = font_menu.render("APPUYEZ SUR ESPACE POUR COMMENCER", True, Blanc)
        screen.blit(txt_msg, txt_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

    elif etape == "MENU_CHOIX":
        screen.blit(image_fond_menu, (0, 0)) 
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
        screen.blit(image_desert, (0, 0))  
        screen.blit(img_helico1, (h1_x, h1_y))
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        txt_attente = font_menu.render("EN ATTENTE JOUEUR 2", True, Blanc)
        txt_action = font_sub.render("appuyer sur espace pour rejoindre", True, Gris)
        screen.blit(txt_attente, txt_attente.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(txt_action, txt_action.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))
        if bouton_retour.collidepoint(mouse_pos):
            c_retour = Gris_fonce
        else:
            c_retour = Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        t_retour = font_menu.render("RETOUR", True, Noir)
        screen.blit(t_retour, (bouton_retour.x + 45, bouton_retour.y + 15))

    elif etape == "ATTENTE":
        screen.blit(image_desert, (0, 0))  # Fond desert ici
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        txt_wait = font_menu.render("RECHERCHE D'UN ADVERSAIRE...", True, Blanc)
        screen.blit(txt_wait, txt_wait.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))
        if bouton_retour.collidepoint(mouse_pos):
            c_retour = Gris_fonce
        else:
            c_retour = Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        t_retour = font_menu.render("RETOUR", True, Noir)
        screen.blit(t_retour, (bouton_retour.x + 45, bouton_retour.y + 15))


    elif etape == "EN_JEU":
        screen.blit(image_desert, (0, 0))
        temps_ecoule = pygame.time.get_ticks() - temps_debut_match

        secondes = (temps_ecoule // 1000) % 60
        minutes = (temps_ecoule // 60000)

        texte_chrono = f"{minutes:02d}:{secondes:02d}"
        surf_chrono = font_menu.render(texte_chrono, True, Blanc)
        screen.blit(surf_chrono, (SCREEN_WIDTH // 2 - 40, 20))

        if helico1.lives <= 0 or helico2.lives <= 0:
            if helico1.lives <= 0:
                winner_text = "VICTOIRE JOUEUR 2"
                helico_mort = helico1
            else:
                winner_text = "VICTOIRE JOUEUR 1"
                helico_mort = helico2

            # On fige le temps affiché
            temps_final = texte_chrono
            explosion_start_time = pygame.time.get_ticks()
            etape = "EXPLOSION"

        txt_vie_j1 = font_sub.render(f"Joueur 1:", True, Blanc)
        txt_vie_j2 = font_sub.render(f"Joueur 2:", True, Blanc)
        txt_vie_j1_rect = txt_vie_j1.get_rect(topleft=(20, 20))
        reserve_coeurs_j2 = 10 + image_coeur.get_width() + max(0, helico2.lives - 1) * 30 + 15 + image_cadre.get_width()
        txt_vie_j2_rect = txt_vie_j2.get_rect(topright=(SCREEN_WIDTH - 20 - reserve_coeurs_j2, 20))
        screen.blit(txt_vie_j1, txt_vie_j1_rect)
        screen.blit(txt_vie_j2, txt_vie_j2_rect)

        for i in range(helico1.lives):
            coeur_j1_rect = image_coeur.get_rect(midleft=(txt_vie_j1_rect.right + 10 + i * 30, txt_vie_j1_rect.centery))
            screen.blit(image_coeur, coeur_j1_rect)

        for i in range(helico2.lives):
            coeur_j2_rect = image_coeur.get_rect(midleft=(txt_vie_j2_rect.right + 10 + i * 30, txt_vie_j2_rect.centery))
            screen.blit(image_coeur, coeur_j2_rect)

        for i in range (helico1.lives):
            coeur_j1_rect = image_coeur.get_rect(midleft=(txt_vie_j1_rect.right + 10 + i*30, txt_vie_j1_rect.centery))
            screen.blit(image_coeur, coeur_j1_rect)
        for i in range (helico2.lives):
            coeur_j2_rect = image_coeur.get_rect(midleft=(txt_vie_j2_rect.right + 10 + i*30, txt_vie_j2_rect.centery))
            screen.blit(image_coeur, coeur_j2_rect)

        if helico1.lives > 0:
            coeurs_j1_fin = txt_vie_j1_rect.right + 10 + (helico1.lives - 1) * 30 + image_coeur.get_width()
        else:
            coeurs_j1_fin = txt_vie_j1_rect.right

        if helico2.lives > 0:
            coeurs_j2_fin = txt_vie_j2_rect.right + 10 + (helico2.lives - 1) * 30 + image_coeur.get_width()
        else:
            coeurs_j2_fin = txt_vie_j2_rect.right

        cadre_j1_rect = image_cadre.get_rect(midleft=(coeurs_j1_fin + 15, txt_vie_j1_rect.centery))
        cadre_j2_rect = image_cadre.get_rect(midleft=(coeurs_j2_fin + 15, txt_vie_j2_rect.centery))

        screen.blit(image_cadre, cadre_j1_rect)
        screen.blit(image_cadre, cadre_j2_rect)

        bonus_j1 = get_current_bonus(helico1)
        bonus_j2 = get_current_bonus(helico2)

        if bonus_j1:
            icon_j1 = bonus_icons_hud[bonus_j1]
            icon_j1_rect = icon_j1.get_rect(center=cadre_j1_rect.center)
            screen.blit(icon_j1, icon_j1_rect)

        if bonus_j2:
            icon_j2 = bonus_icons_hud[bonus_j2]
            icon_j2_rect = icon_j2.get_rect(center=cadre_j2_rect.center)
            screen.blit(icon_j2, icon_j2_rect)


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

            for projectile in obs.projectiles[:]:
                pygame.draw.rect(screen, (255, 0, 0), projectile)
                if projectile.colliderect(helico1.rect):
                    helico1.take_damage()
                    obs.projectiles.remove(projectile)
                elif projectile.colliderect(helico2.rect):
                    helico2.take_damage()
                    obs.projectiles.remove(projectile)

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
        print(helico1.lives, helico2.lives)
        screen.blit(helico1.image, helico1.rect)
        screen.blit(helico2.image, helico2.rect)
        if helico1.check_collision(helico2):
           helico2.image.set_alpha(128)
        else:
           helico2.image.set_alpha(255)

    elif etape == "EXPLOSION":
        screen.blit(image_desert, (0, 0))

        if helico_mort is helico1:
            screen.blit(helico2.image, helico2.rect)
        elif helico_mort is helico2:
            screen.blit(helico1.image, helico1.rect)

        if helico_mort is not None:
            frame_index = (pygame.time.get_ticks() // 100) % len(gif_explosion)
            explosion_rect = gif_explosion[frame_index].get_rect(center=helico_mort.rect.center)
            screen.blit(gif_explosion[frame_index], explosion_rect)

        if explosion_start_time is not None and pygame.time.get_ticks() - explosion_start_time >= explosion_duration_ms:
            etape = "GAME_OVER"

    elif etape == "GAME_OVER":
        # 1. On affiche le fond (le même que le menu)
        screen.blit(image_fond_menu, (0, 0))

        # 2. On ajoute un voile noir transparent par-dessus pour faire ressortir le texte
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))  # Noir avec une forte opacité
        screen.blit(overlay, (0, 0))

        # 3. Affichage du vainqueur (en gros avec font_titre)
        t_win = font_titre.render(winner_text, True, Vert)
        screen.blit(t_win, t_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        # 4. Affichage du chrono final (temps_final qu'on a figé à la mort)
        t_temps = font_menu.render(f"TEMPS DE SURVIE : {temps_final}", True, Blanc)
        screen.blit(t_temps, t_temps.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # 5. Dessin du bouton REJOUER
        if bouton_rejouer.collidepoint(mouse_pos):
            c_rej = Gris_fonce
        else:
            c_rej = Gris

        pygame.draw.rect(screen, c_rej, bouton_rejouer, border_radius=10)
        t_rej = font_menu.render("REJOUER", True, Noir)
        # Placement manuel du texte dans le bouton (x + 55, y + 15)
        t_rej_rect = t_rej.get_rect(center=bouton_rejouer.center)
        screen.blit(t_rej, t_rej_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()