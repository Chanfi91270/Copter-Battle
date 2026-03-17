import pygame

# --- INITIALISATION ---
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Copter Battle")
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

image_fond = pygame.image.load('./images/fond(1).png').convert()
image_fond = pygame.transform.scale(image_fond, (SCREEN_WIDTH, SCREEN_HEIGHT))

Vert = (120, 150, 80)
Blanc = (255, 255, 255)
Noir = (0, 0, 0)
Gris = (200, 200, 200)
Gris_fonce = (100, 100, 100)

font_titre = pygame.font.SysFont("Impact", 150)
font_menu = pygame.font.SysFont("Arial", 30, bold=True)

bouton_lancer = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 220, 70)
bouton_rejoindre = pygame.Rect(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2 + 50, 220, 70)

etape = "ACCUEIL"  # ACCUEIL, MENU_CHOIX, EN_JEU

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Gestion des étapes
            if etape == "ACCUEIL" and event.key == pygame.K_SPACE:
                etape = "MENU_CHOIX"

        if etape == "MENU_CHOIX" and event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_lancer.collidepoint(mouse_pos) or bouton_rejoindre.collidepoint(mouse_pos):
                etape = "EN_JEU"

    # 2. fill the screen to wipe away anything from last frame
    screen.blit(image_fond, (0, 0))

    # 3. Affichage selon l'étape
    if etape == "ACCUEIL":
        # Titre Vert Camo (Simple)
        txt_titre = font_titre.render("COPTER BATTLE", True, Vert)
        rect_titre = txt_titre.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(txt_titre, rect_titre)

        txt_msg = font_menu.render("APPUYEZ SUR ESPACE POUR COMMENCER", True, Blanc)
        rect_msg = txt_msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(txt_msg, rect_msg)

    elif etape == "MENU_CHOIX":
        # Voile sombre
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Dessin des boutons (LANCER / REJOINDRE)
        for btn, txt in [(bouton_lancer, "LANCER"), (bouton_rejoindre, "REJOINDRE")]:
            couleur = Gris_fonce if btn.collidepoint(mouse_pos) else Gris
            pygame.draw.rect(screen, couleur, btn, border_radius=10)
            txt_surf = font_menu.render(txt, True, Noir)
            screen.blit(txt_surf, (btn.centerx - txt_surf.get_width() // 2, btn.centery - txt_surf.get_height() // 2))

    elif etape == "EN_JEU":
        # Pour l'instant, on dessine leur rectangle blanc de test sans recréer la fenêtre
        pygame.draw.rect(pygame.display.set_mode((500,300)),(Blanc),[100,100,150,150])

    # 4. flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()