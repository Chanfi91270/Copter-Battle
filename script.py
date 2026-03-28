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
#Images pour hélicos

img_helico1 = pygame.image.load('./images/helicoJ1.png').convert_alpha()
img_helico1 = pygame.transform.scale(img_helico1, (110, 90))

img_helico2 = pygame.image.load('./images/helicoJ2.png').convert_alpha()
img_helico2 = pygame.transform.scale(img_helico2, (110, 90))

gif_chargement = []
for i in range(1, 9):  
    img = pygame.image.load(f'./images/gif/loading_{i}.png').convert_alpha()
    gif_chargement.append(img)

touches_j1 = {"gauche": pygame.K_q, "droite": pygame.K_d, "haut": pygame.K_z, "bas": pygame.K_s, "bonus": pygame.K_a}
touches_j2 = {"gauche": pygame.K_LEFT, "droite": pygame.K_RIGHT, "haut": pygame.K_UP, "bas": pygame.K_DOWN, "bonus": pygame.K_RSHIFT}

helico1 = Helicopter(50, 100, False, LIVES, img_helico1, touches_j1)
helico2 = Helicopter(50, SCREEN_HEIGHT - 250, False, LIVES,img_helico2, touches_j2)

#Images pour obstacles
img_rock = pygame.image.load('./images/rock.png').convert_alpha()
img_rock = pygame.transform.scale(img_rock, (120, 120))
img_avion = pygame.image.load('./images/avion.png').convert_alpha()
img_avion = pygame.transform.scale(img_avion, (110, 90))

images_obstacles = {
    "rock": img_rock,
    "avion": img_avion
}

obstacles = []
spawn_timer = 0


img_bonus_bombe = pygame.image.load('./images/bombe.png').convert_alpha()
img_bonus_bombe = pygame.transform.scale(img_bonus_bombe, (100, 100))
img_bonus_rafale = pygame.image.load('./images/rafale_tir.png').convert_alpha()
img_bonus_rafale = pygame.transform.scale(img_bonus_rafale, (100, 100))
img_bonus_bouclier = pygame.image.load('./images/bouclier.png').convert_alpha()
img_bonus_bouclier = pygame.transform.scale(img_bonus_bouclier, (100, 100))

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
bouton_retour = pygame.Rect(30, SCREEN_HEIGHT - 80, 180, 60)
bouton_rejouer = pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 100, 220, 70)


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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if etape == "MENU_CHOIX":
                if bouton_lancer.collidepoint(mouse_pos): etape = "ATTENTE_J2"
                elif bouton_rejoindre.collidepoint(mouse_pos): etape = "ATTENTE"
            elif etape in ["ATTENTE_J2", "ATTENTE"]:
                if bouton_retour.collidepoint(mouse_pos): etape = "MENU_CHOIX"
            elif etape == "GAME_OVER":
                if bouton_rejouer.collidepoint(mouse_pos):
                    helico1.rect.topleft = (50, 100)
                    helico2.rect.topleft = (50, SCREEN_HEIGHT - 250)
                    helico1.lives, helico2.lives = 3, 3
                    obstacles.clear()
                    bonuses.clear()
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

        for btn, txt in [(bouton_lancer, "LANCER"), (bouton_rejoindre, "REJOINDRE")]:
            c = Gris_fonce if btn.collidepoint(mouse_pos) else Gris
            pygame.draw.rect(screen, c, btn, border_radius=10)
            screen.blit(font_menu.render(txt, True, Noir), font_menu.render(txt, True, Noir).get_rect(center=btn.center))

    elif etape == "ATTENTE_J2":
        screen.blit(image_desert, (0, 0))  
        screen.blit(img_helico1, (h1_x, h1_y))
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        screen.blit(font_menu.render("EN ATTENTE JOUEUR 2", True, Blanc), font_menu.render("EN ATTENTE JOUEUR 2", True, Blanc).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(font_sub.render("appuyer sur espace pour rejoindre", True, Gris), font_sub.render("appuyer sur espace pour rejoindre", True, Gris).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))
        c_ret = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_ret, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), font_menu.render("RETOUR", True, Noir).get_rect(center=bouton_retour.center))

    elif etape == "ATTENTE":
        screen.blit(image_desert, (0, 0))  
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        screen.blit(font_menu.render("RECHERCHE D'UN ADVERSAIRE...", True, Blanc), font_menu.render("RECHERCHE D'UN ADVERSAIRE...", True, Blanc).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))
        c_ret = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_ret, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), font_menu.render("RETOUR", True, Noir).get_rect(center=bouton_retour.center))

    elif etape == "EN_JEU":
        screen.blit(image_desert, (0, 0))
        millisecondes = pygame.time.get_ticks() - temps_debut_match
        texte_chrono = f"{(millisecondes // 60000):02d}:{(millisecondes // 1000 % 60):02d}"
        surf_chrono = font_menu.render(texte_chrono, True, Blanc)
        rect_chrono = surf_chrono.get_rect(midtop=(SCREEN_WIDTH // 2, 20))
        pygame.draw.rect(screen, (0, 0, 0, 150), rect_chrono.inflate(20, 10), border_radius=5)
        screen.blit(surf_chrono, rect_chrono)

        t_j1 = font_sub.render("Joueur 1:", True, Blanc)
        r_j1 = t_j1.get_rect(topleft=(20, 20))
        screen.blit(t_j1, r_j1)
        for i in range(helico1.lives): screen.blit(image_coeur, (r_j1.right + 10 + i*30, r_j1.top))

        t_j2 = font_sub.render("Joueur 2:", True, Blanc)
        r_j2 = t_j2.get_rect(topright=(SCREEN_WIDTH - 20 - (10 + 25 + max(0, helico2.lives-1)*30), 20))
        screen.blit(t_j2, r_j2)
        for i in range(helico2.lives): screen.blit(image_coeur, (r_j2.right + 10 + i*30, r_j2.top))            

        coeurs_j1_fin = r_j1.right + 10 + (helico1.lives * 30)
        cadre_j1_rect = image_cadre.get_rect(midleft=(coeurs_j1_fin + 15, r_j1.centery))
        cadre_j2_rect = image_cadre.get_rect(midright=(r_j2.left - 15, r_j2.centery))
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
        if spawn_timer >= 120:  
            obstacles.append(spawn_obstacle(SCREEN_WIDTH, SCREEN_HEIGHT, images_obstacles))
            spawn_timer = 0

        bonus_spawn_timer += 1
        if bonus_spawn_timer >= 180:  
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
            bonus.move(); screen.blit(bonus.image, bonus.rect)
            if bonus.check_collision(helico1): bonus.apply(helico1)
            elif bonus.check_collision(helico2): bonus.apply(helico2)

        obstacles = [o for o in obstacles if not o.hitbox.right < 0 and not o.is_dead()]

        bonuses = [b for b in bonuses if not b.rect.right < 0 and b.active]

        helico1.move(SCREEN_WIDTH, SCREEN_HEIGHT); helico2.move(SCREEN_WIDTH, SCREEN_HEIGHT)
        if helico1.is_transparent:
            helico1.image.set_alpha(128)
        else:
            helico1.image.set_alpha(255)

        if helico2.is_transparent or (helico1.check_collision(helico2) and not helico1.is_transparent):
            helico2.image.set_alpha(128)
        else:
            helico2.image.set_alpha(255)

        if helico1.lives <= 0 or helico2.lives <= 0:
            winner_text = "VICTOIRE JOUEUR 2" if helico1.lives <= 0 else "VICTOIRE JOUEUR 1"
            temps_final = texte_chrono
            etape = "GAME_OVER"

    elif etape == "GAME_OVER":
        screen.blit(image_fond_menu, (0, 0))
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA); ov.fill((0, 0, 0, 200))
        screen.blit(ov, (0, 0))
        tw = font_titre.render(winner_text, True, Vert)
        screen.blit(tw, tw.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
        ts = font_menu.render(f"TEMPS DE SURVIE : {temps_final}", True, Blanc)
        screen.blit(ts, ts.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        c_rj = Gris_fonce if bouton_rejouer.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_rj, bouton_rejouer, border_radius=10)
        screen.blit(font_menu.render("REJOUER", True, Noir), font_menu.render("REJOUER", True, Noir).get_rect(center=bouton_rejouer.center))
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()