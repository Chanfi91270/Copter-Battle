import pygame


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Copter Battle")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    
    pygame.draw.rect(pygame.display.set_mode((500,300)),(255,255,255),[100,100,150,150])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
