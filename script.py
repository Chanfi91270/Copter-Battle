import pygame
from classes.helico import Helicopter
from classes.obstacle import spawn_obstacle
from classes.bonus import spawn_bonus
from classes.joueur import Joueur

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Copter Battle")
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

temps_debut_match = 0
winner_text = ""
temps_final = ""
h1_x, h1_y = 50, 100
h2_x, h2_y = 50, SCREEN_HEIGHT - 250
LIVES = 3

# Mode de jeu : "local" ou "enligne"
mode_jeu = "local"

# Joueur local (initialisé plus tard selon le choix)
joueur_local = None

# Saisie IP pour rejoindre
ip_saisie = ""
ip_active = False

# Images pour fond
image_fond_menu = pygame.image.load('./images/fond_accueil.png').convert()
image_fond_menu = pygame.transform.scale(image_fond_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

image_desert = pygame.image.load('./images/fond_jeu.png').convert()
image_desert = pygame.transform.scale(image_desert, (SCREEN_WIDTH, SCREEN_HEIGHT))

image_coeur = pygame.image.load('./images/coeur.png').convert_alpha()
image_coeur = pygame.transform.scale(image_coeur, (25, 25))

image_cadre = pygame.image.load('./images/cadre.png').convert_alpha()
image_cadre = pygame.transform.scale(image_cadre, (150, 100))

gif_explosion = []
for i in range(1, 6):
    img = pygame.image.load(f'./images/gif_explosion/frame_{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (110, 90))
    gif_explosion.append(img)

# Images pour hélicos
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

helico1 = Helicopter(50, 100, False, LIVES, img_helico1, touches_j1)
helico2 = Helicopter(50, SCREEN_HEIGHT - 250, False, LIVES, img_helico2, touches_j2)

# Images pour obstacles
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
active_bombs = []
BOMB_SPEED = 8
BOMB_FUSE_MS = 700
BOMB_EXPLOSION_MS = 350
BOMB_ZONE_SIZE = (170, 140)
active_player_projectiles = []
pending_rafales = []
PLAYER_SHOT_SPEED = 10
RAFALE_INTERVAL_MS = 120

img_bonus_bombe = pygame.image.load('./images/bombe.png').convert_alpha()
img_bonus_bombe = pygame.transform.scale(img_bonus_bombe, (60, 80))
img_bonus_rafale = pygame.image.load('./images/rafale_tir.png').convert_alpha()
img_bonus_rafale = pygame.transform.scale(img_bonus_rafale, (60, 50))
img_bonus_bouclier = pygame.image.load('./images/bouclier.png').convert_alpha()
img_bonus_bouclier = pygame.transform.scale(img_bonus_bouclier, (70, 70))
img_bulle_bouclier = pygame.image.load('./images/bulle_bouclier.png').convert_alpha()
img_bulle_bouclier = pygame.transform.scale(img_bulle_bouclier, (150, 130))
img_bulle_bouclier.set_alpha(128)

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
Rouge = (200, 60, 60)

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


def apply_bonus_effect(helico, bonus_type, obstacles):
    if bonus_type == "bombe":
        bomb_rect = img_bonus_bombe.get_rect(midright=(helico.rect.left, helico.rect.centery))
        active_bombs.append({
            "rect": bomb_rect,
            "spawn_time": pygame.time.get_ticks(),
            "exploded": False,
            "explosion_start": 0,
            "damage_done": False,
        })
    elif bonus_type == "rafale":
        pending_rafales.append({
            "helico": helico,
            "remaining": helico.nb_rafale,
            "next_fire": pygame.time.get_ticks(),
        })
    elif bonus_type == "bouclier":
        helico.set_transparency(True)
        helico.transparent_until = pygame.time.get_ticks() + helico.temps_bouclier
        helico.activate_shield_visual()


def reinitialiser_jeu():
    """Remet tout à zéro pour rejouer."""
    global spawn_timer, bonus_spawn_timer, helico_mort, explosion_start_time, winner_text, temps_final
    helico1.lives = LIVES
    helico2.lives = LIVES
    helico1.rect.topleft = (50, 100)
    helico2.rect.topleft = (50, SCREEN_HEIGHT - 250)
    for h in [helico1, helico2]:
        h.bonus_shield = False
        h.bonus_bombes = False
        h.bonus_rafale = False
        h.set_transparency(False)
        h.transparent_until = 0
        h.shield_visual_until = 0
        h.pending_bonus = None
        h.bonus_key_was_pressed = False
    obstacles.clear()
    bonuses.clear()
    active_bombs.clear()
    active_player_projectiles.clear()
    pending_rafales.clear()
    spawn_timer = 0
    bonus_spawn_timer = 0
    helico_mort = None
    explosion_start_time = None
    winner_text = ""
    temps_final = ""


def appliquer_etat_reseau(etat):
    
    # Hélico 1
    h1 = etat["h1"]
    helico1.rect.x = h1["x"]
    helico1.rect.y = h1["y"]
    helico1.lives = h1["vies"]
    helico1.is_transparent = h1["transparent"]
    helico1.image.set_alpha(128 if h1["transparent"] else 255)
    if h1["shield_visuel"]:
        helico1.shield_visual_until = pygame.time.get_ticks() + 100
    helico1.bonus_bombes = h1["bonus"] == "bombe"
    helico1.bonus_rafale = h1["bonus"] == "rafale"
    helico1.bonus_shield = h1["bonus"] == "bouclier"

    # Hélico 2
    h2 = etat["h2"]
    helico2.rect.x = h2["x"]
    helico2.rect.y = h2["y"]
    helico2.lives = h2["vies"]
    helico2.is_transparent = h2["transparent"]
    helico2.image.set_alpha(128 if h2["transparent"] else 255)
    if h2["shield_visuel"]:
        helico2.shield_visual_until = pygame.time.get_ticks() + 100
    helico2.bonus_bombes = h2["bonus"] == "bombe"
    helico2.bonus_rafale = h2["bonus"] == "rafale"
    helico2.bonus_shield = h2["bonus"] == "bouclier"

    # Obstacles (on reconstruit la liste de hitbox pour l'affichage)
    obstacles.clear()
    for o_data in etat["obstacles"]:
        # On crée un obstacle factice juste pour l'affichage
        obs_rect = pygame.Rect(o_data["x"], o_data["y"], o_data["w"], o_data["h"])
        # Déterminer l'image selon la taille
        if o_data["w"] == 120 and o_data["h"] == 90:
            img = img_avion
        else:
            img = img_rock
        # Stocker comme objet simple pour le rendu
        class ObsFactice:
            pass
        obs = ObsFactice()
        obs.hitbox = obs_rect
        obs.image = img
        obs.projectiles = [
            pygame.Rect(p["x"], p["y"], p["w"], p["h"])
            for p in o_data.get("projectiles", [])
        ]
        obstacles.append(obs)
    # Bombes
    active_bombs.clear()
    for b in etat.get("bombes", []):
        active_bombs.append({
            "rect": pygame.Rect(b["x"], b["y"], 60, 80),
            "spawn_time": b["spawn_time"],
            "exploded": b["exploded"],
            "explosion_start": b["explosion_start"],
            "damage_done": True,  # le serveur gère les dégâts, pas le client
        })

    # Projectiles joueurs
    active_player_projectiles.clear()
    for s in etat.get("projectiles", []):
        active_player_projectiles.append({
            "rect": pygame.Rect(s["x"], s["y"], s["w"], s["h"]),
            "direction": 1,
            "owner": None,  # pas besoin côté client, juste pour l'affichage
        })
    # Bonus au sol
    bonuses.clear()
    for b_data in etat.get("bonus_sol", []):
        if b_data["active"]:
            img = images_bonus[b_data["type"]]
            from classes.bonus import Bonus
            b = Bonus(b_data["x"], b_data["y"], img, b_data["type"])
            bonuses.append(b)


bouton_lancer = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 220, 70)
bouton_rejoindre = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50, 220, 70)
bouton_retour = pygame.Rect(30, SCREEN_HEIGHT - 100, 200, 70)
bouton_rejouer = pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 100, 220, 70)
champ_ip = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30, 300, 50)

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
                # Fermer la connexion proprement si on quitte
                if joueur_local:
                    joueur_local.close_connection()
                running = False

            if etape == "ACCUEIL" and event.key == pygame.K_SPACE:
                etape = "MENU_CHOIX"

            # Saisie IP dans l'écran REJOINDRE
            elif etape == "SAISIE_IP":
                if ip_active:
                    if event.key == pygame.K_RETURN:
                        # Lancer la connexion client
                        joueur_local = Joueur("Joueur 2", 2, server=False)
                        joueur_local.set_helico(helico2)
                        joueur_local.set_join(ip=ip_saisie)
                        mode_jeu = "enligne"
                        etape = "CONNEXION_CLIENT"
                    elif event.key == pygame.K_BACKSPACE:
                        ip_saisie = ip_saisie[:-1]
                    else:
                        if len(ip_saisie) < 15:
                            ip_saisie += event.unicode

            # Mode local : ESPACE pour lancer en ATTENTE_J2
            elif etape == "ATTENTE_J2" and mode_jeu == "local" and event.key == pygame.K_SPACE:
                etape = "EN_JEU"
                temps_debut_match = pygame.time.get_ticks()

        # Clics souris
        if event.type == pygame.MOUSEBUTTONDOWN:

            if etape == "MENU_CHOIX":
                if bouton_lancer.collidepoint(mouse_pos):
                    # Mode local (comme avant)
                    mode_jeu = "local"
                    joueur_local = None
                    etape = "ATTENTE_J2"
                elif bouton_rejoindre.collidepoint(mouse_pos):
                    # Mode en ligne — choix : héberger ou rejoindre
                    etape = "MENU_ENLIGNE"

            elif etape == "MENU_ENLIGNE":
                bouton_heberger = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 220, 70)
                bouton_rejoindre2 = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50, 220, 70)
                if bouton_heberger.collidepoint(mouse_pos):
                    # Créer le serveur
                    joueur_local = Joueur("Joueur 1", 1, server=True)
                    joueur_local.set_helico(helico1)
                    joueur_local.set_join()
                    mode_jeu = "enligne"
                    etape = "ATTENTE_CONNEXION"
                elif bouton_rejoindre2.collidepoint(mouse_pos):
                    # Aller à la saisie IP
                    ip_saisie = ""
                    ip_active = True
                    etape = "SAISIE_IP"

            if (etape in ("ATTENTE_J2", "ATTENTE", "ATTENTE_CONNEXION", "CONNEXION_CLIENT", "SAISIE_IP", "MENU_ENLIGNE")
                    and bouton_retour.collidepoint(mouse_pos)):
                if joueur_local:
                    joueur_local.close_connection()
                    joueur_local = None
                mode_jeu = "local"
                etape = "MENU_CHOIX"

            if etape == "GAME_OVER" and bouton_rejouer.collidepoint(mouse_pos):
                reinitialiser_jeu()
                if mode_jeu == "enligne":
                    etape = "ATTENTE_CONNEXION" if joueur_local and joueur_local.est_server() else "CONNEXION_CLIENT"
                else:
                    etape = "ATTENTE_J2"

        if etape == "SAISIE_IP" and event.type == pygame.MOUSEBUTTONDOWN:
            ip_active = champ_ip.collidepoint(mouse_pos)

    if etape == "ATTENTE_CONNEXION" and joueur_local:
        # Serveur attend que le client se connecte
        if joueur_local.accepter_connexion():
            etape = "EN_JEU"
            temps_debut_match = pygame.time.get_ticks()

    if etape == "CONNEXION_CLIENT" and joueur_local:
        # Client tente de se connecter
        if joueur_local.verifier_connexion():
            etape = "EN_JEU"
            temps_debut_match = pygame.time.get_ticks()


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

        c_lancer = Gris_fonce if bouton_lancer.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_lancer, bouton_lancer, border_radius=10)
        screen.blit(font_menu.render("LOCAL", True, Noir), font_menu.render("LOCAL", True, Noir).get_rect(center=bouton_lancer.center))

        c_rejoindre = Gris_fonce if bouton_rejoindre.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_rejoindre, bouton_rejoindre, border_radius=10)
        screen.blit(font_menu.render("EN LIGNE", True, Noir), font_menu.render("EN LIGNE", True, Noir).get_rect(center=bouton_rejoindre.center))

    elif etape == "MENU_ENLIGNE":
        screen.blit(image_fond_menu, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt = font_menu.render("MODE EN LIGNE", True, Blanc)
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))

        bouton_heberger = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 220, 70)
        bouton_rejoindre2 = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50, 220, 70)

        c_heb = Gris_fonce if bouton_heberger.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_heb, bouton_heberger, border_radius=10)
        screen.blit(font_menu.render("HÉBERGER", True, Noir), font_menu.render("HÉBERGER", True, Noir).get_rect(center=bouton_heberger.center))

        c_rej2 = Gris_fonce if bouton_rejoindre2.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_rej2, bouton_rejoindre2, border_radius=10)
        screen.blit(font_menu.render("REJOINDRE", True, Noir), font_menu.render("REJOINDRE", True, Noir).get_rect(center=bouton_rejoindre2.center))

        c_retour = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), (bouton_retour.x + 45, bouton_retour.y + 15))

    elif etape == "SAISIE_IP":
        screen.blit(image_fond_menu, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        txt = font_menu.render("ENTREZ L'IP DU SERVEUR :", True, Blanc)
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))

        couleur_champ = Blanc if ip_active else Gris
        pygame.draw.rect(screen, couleur_champ, champ_ip, border_radius=8)
        pygame.draw.rect(screen, Noir, champ_ip, 2, border_radius=8)
        txt_ip = font_menu.render(ip_saisie, True, Noir)
        screen.blit(txt_ip, (champ_ip.x + 10, champ_ip.y + 10))

        txt_hint = font_sub.render("Appuyez sur ENTRÉE pour confirmer", True, Gris)
        screen.blit(txt_hint, txt_hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

        c_retour = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), (bouton_retour.x + 45, bouton_retour.y + 15))

    elif etape == "ATTENTE_CONNEXION":
        screen.blit(image_desert, (0, 0))
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))

        txt = font_menu.render("EN ATTENTE D'UN ADVERSAIRE...", True, Blanc)
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # Afficher l'IP locale pour que l'adversaire puisse se connecter
        import socket as _socket
        try:
            ip_locale = _socket.gethostbyname(_socket.gethostname())
        except Exception:
            ip_locale = "?"
        txt_ip = font_sub.render(f"Votre IP : {ip_locale}", True, Gris)
        screen.blit(txt_ip, txt_ip.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

        c_retour = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), (bouton_retour.x + 45, bouton_retour.y + 15))

    elif etape == "CONNEXION_CLIENT":
        screen.blit(image_desert, (0, 0))
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))

        txt = font_menu.render(f"CONNEXION À {ip_saisie}...", True, Blanc)
        screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        c_retour = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), (bouton_retour.x + 45, bouton_retour.y + 15))

    elif etape == "ATTENTE_J2":
        screen.blit(image_desert, (0, 0))
        screen.blit(img_helico1, (h1_x, h1_y))
        frame_index = (pygame.time.get_ticks() // 100) % len(gif_chargement)
        txt_attente = font_menu.render("EN ATTENTE JOUEUR 2", True, Blanc)
        txt_action = font_sub.render("Appuyez sur ESPACE pour commencer", True, Gris)
        screen.blit(txt_attente, txt_attente.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(txt_action, txt_action.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
        screen.blit(gif_chargement[frame_index], (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150))
        c_retour = Gris_fonce if bouton_retour.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_retour, bouton_retour, border_radius=10)
        screen.blit(font_menu.render("RETOUR", True, Noir), (bouton_retour.x + 45, bouton_retour.y + 15))

    elif etape == "EN_JEU":
        screen.blit(image_desert, (0, 0))

        # MODE EN LIGNE
        if mode_jeu == "enligne" and joueur_local:

            if joueur_local.est_server():
                # SERVEUR : reçoit les touches du client, calcule le jeu, envoie l'état
                joueur_local.recevoir_touches()
                helico2.move_reseau(joueur_local.touches_distantes, SCREEN_WIDTH, SCREEN_HEIGHT)
                helico1.move(SCREEN_WIDTH, SCREEN_HEIGHT)

            else:
                # CLIENT : envoie ses touches, reçoit et applique l'état
                keys = pygame.key.get_pressed()
                touches = {
                    "gauche": bool(keys[touches_j2["gauche"]]),
                    "droite": bool(keys[touches_j2["droite"]]),
                    "haut":   bool(keys[touches_j2["haut"]]),
                    "bas":    bool(keys[touches_j2["bas"]]),
                    "bonus":  bool(keys[touches_j2["bonus"]]),
                }
                joueur_local.envoyer_touches(touches)
                etat = joueur_local.recevoir_etat()
                if etat:
                    appliquer_etat_reseau(etat)

        # CHRONO 
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
            temps_final = texte_chrono
            explosion_start_time = pygame.time.get_ticks()
            etape = "EXPLOSION"

        txt_vie_j1 = font_sub.render("Joueur 1:", True, Blanc)
        txt_vie_j2 = font_sub.render("Joueur 2:", True, Blanc)
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

        coeurs_j1_fin = txt_vie_j1_rect.right + 10 + max(0, helico1.lives - 1) * 30 + image_coeur.get_width() if helico1.lives > 0 else txt_vie_j1_rect.right
        coeurs_j2_fin = txt_vie_j2_rect.right + 10 + max(0, helico2.lives - 1) * 30 + image_coeur.get_width() if helico2.lives > 0 else txt_vie_j2_rect.right

        cadre_j1_rect = image_cadre.get_rect(midleft=(coeurs_j1_fin + 15, txt_vie_j1_rect.centery))
        cadre_j2_rect = image_cadre.get_rect(midleft=(coeurs_j2_fin + 15, txt_vie_j2_rect.centery))
        screen.blit(image_cadre, cadre_j1_rect)
        screen.blit(image_cadre, cadre_j2_rect)

        bonus_j1 = get_current_bonus(helico1)
        bonus_j2 = get_current_bonus(helico2)
        if bonus_j1:
            icon_j1 = bonus_icons_hud[bonus_j1]
            screen.blit(icon_j1, icon_j1.get_rect(center=cadre_j1_rect.center))
        if bonus_j2:
            icon_j2 = bonus_icons_hud[bonus_j2]
            screen.blit(icon_j2, icon_j2.get_rect(center=cadre_j2_rect.center))

        if mode_jeu == "local" or (mode_jeu == "enligne" and joueur_local and joueur_local.est_server()):

            # Mode local : bouger helico1 et helico2 normalement
            if mode_jeu == "local":
                helico1.move(SCREEN_WIDTH, SCREEN_HEIGHT)
                helico2.move(SCREEN_WIDTH, SCREEN_HEIGHT)

            spawn_timer += 1
            if spawn_timer >= 120:
                obstacles.append(spawn_obstacle(SCREEN_WIDTH, SCREEN_HEIGHT, images_obstacles))
                spawn_timer = 0

            bonus_spawn_timer += 1
            if bonus_spawn_timer >= 180:
                bonuses.append(spawn_bonus(SCREEN_WIDTH, SCREEN_HEIGHT, images_bonus))
                bonus_spawn_timer = 0

            # Obstacles
            for obs in obstacles:
                obs.move()
                obs.shoot()
                obs.update_projectiles()

                for projectile in obs.projectiles[:]:
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

            # Bonus
            for bonus in bonuses:
                bonus.move()
                if bonus.check_collision(helico1):
                    bonus.apply(helico1)
                elif bonus.check_collision(helico2):
                    bonus.apply(helico2)

            obstacles = [o for o in obstacles if not o.hitbox.right < 0 and not o.is_dead()]
            bonuses = [b for b in bonuses if not b.rect.right < 0 and b.active]

            # Bombes
            now = pygame.time.get_ticks()
            for bomb in active_bombs[:]:
                if not bomb["exploded"]:
                    bomb["rect"].x -= BOMB_SPEED
                    if now - bomb["spawn_time"] >= BOMB_FUSE_MS:
                        bomb["exploded"] = True
                        bomb["explosion_start"] = now
                else:
                    zone_rect = pygame.Rect(0, 0, BOMB_ZONE_SIZE[0], BOMB_ZONE_SIZE[1])
                    zone_rect.center = bomb["rect"].center
                    if not bomb["damage_done"]:
                        if zone_rect.colliderect(helico1.rect):
                            helico1.take_damage()
                        if zone_rect.colliderect(helico2.rect):
                            helico2.take_damage()
                        for obs in obstacles:
                            if zone_rect.colliderect(obs.hitbox):
                                while not obs.is_dead():
                                    obs.take_damage()
                    bomb["damage_done"] = True
                    if now - bomb["explosion_start"] >= BOMB_EXPLOSION_MS:
                        active_bombs.remove(bomb)

            # Rafales
            for burst in pending_rafales[:]:
                if now >= burst["next_fire"] and burst["remaining"] > 0:
                    shooter = burst["helico"]
                    shot_rect = pygame.Rect(0, shooter.rect.centery - 3, 14, 6)
                    shot_rect.left = shooter.rect.right
                    active_player_projectiles.append({"rect": shot_rect, "direction": 1, "owner": shooter})
                    burst["remaining"] -= 1
                    burst["next_fire"] = now + RAFALE_INTERVAL_MS
                if burst["remaining"] <= 0:
                    pending_rafales.remove(burst)

            # Projectiles joueurs
            for shot in active_player_projectiles[:]:
                shot["rect"].x += shot["direction"] * PLAYER_SHOT_SPEED
                hit_obstacle = False
                for obs in obstacles:
                    if shot["rect"].colliderect(obs.hitbox):
                        obs.take_damage()
                        active_player_projectiles.remove(shot)
                        hit_obstacle = True
                        break
                if hit_obstacle:
                    continue
                target = helico2 if shot["owner"] is helico1 else helico1
                if shot["rect"].colliderect(target.rect):
                    target.take_damage()
                    active_player_projectiles.remove(shot)
                    continue
                if shot["rect"].right < 0 or shot["rect"].left > SCREEN_WIDTH:
                    active_player_projectiles.remove(shot)

            obstacles = [o for o in obstacles if not o.is_dead()]

            # Bonus activés
            bonus_used_j1 = helico1.consume_pending_bonus()
            if bonus_used_j1:
                apply_bonus_effect(helico1, bonus_used_j1, obstacles)
            bonus_used_j2 = helico2.consume_pending_bonus()
            if bonus_used_j2:
                apply_bonus_effect(helico2, bonus_used_j2, obstacles)

            # Envoyer l'état au client si en ligne
            if mode_jeu == "enligne" and joueur_local:
                joueur_local.envoyer_etat(helico1, helico2, obstacles, active_bombs, active_player_projectiles, bonuses)

        # RENDU OBSTACLES
        for obs in obstacles:
            screen.blit(obs.image, obs.hitbox)
            for projectile in obs.projectiles:
                pygame.draw.rect(screen, (255, 0, 0), projectile)

        # RENDU BONUS 
        for bonus in bonuses:
            screen.blit(bonus.image, bonus.rect)

        # RENDU BOMBES 
        now = pygame.time.get_ticks()
        for bomb in active_bombs:
            if not bomb["exploded"]:
                screen.blit(img_bonus_bombe, bomb["rect"])
            else:
                zone_rect = pygame.Rect(0, 0, BOMB_ZONE_SIZE[0], BOMB_ZONE_SIZE[1])
                zone_rect.center = bomb["rect"].center
                frame_index = ((now - bomb["explosion_start"]) // 80) % len(gif_explosion)
                explosion_image = pygame.transform.scale(gif_explosion[frame_index], BOMB_ZONE_SIZE)
                screen.blit(explosion_image, explosion_image.get_rect(center=zone_rect.center))

        # RENDU PROJECTILES JOUEURS 
        for shot in active_player_projectiles:
            pygame.draw.rect(screen, (255, 220, 80), shot["rect"])

        # RENDU HÉLICOS 
        screen.blit(helico1.image, helico1.rect)
        screen.blit(helico2.image, helico2.rect)

        if helico1.shield_visual_active():
            screen.blit(img_bulle_bouclier, img_bulle_bouclier.get_rect(center=helico1.rect.center))
        if helico2.shield_visual_active():
            screen.blit(img_bulle_bouclier, img_bulle_bouclier.get_rect(center=helico2.rect.center))

        if helico1.check_collision(helico2):
            if not helico2.is_transparent:
                helico2.image.set_alpha(128)
        else:
            if not helico2.is_transparent:
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
        screen.blit(image_fond_menu, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        t_win = font_titre.render(winner_text, True, Vert)
        screen.blit(t_win, t_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        t_temps = font_menu.render(f"TEMPS DE SURVIE : {temps_final}", True, Blanc)
        screen.blit(t_temps, t_temps.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        c_rej = Gris_fonce if bouton_rejouer.collidepoint(mouse_pos) else Gris
        pygame.draw.rect(screen, c_rej, bouton_rejouer, border_radius=10)
        screen.blit(font_menu.render("REJOUER", True, Noir), font_menu.render("REJOUER", True, Noir).get_rect(center=bouton_rejouer.center))

    pygame.display.flip()
    clock.tick(60)

if joueur_local:
    joueur_local.close_connection()
pygame.quit()