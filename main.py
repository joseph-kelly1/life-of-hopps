import pygame
import constants as c
from hopps import Hopps

# setup pygame

pygame.init()

screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Life of Hopps")

clock = pygame.time.Clock()

# load images
background = pygame.image.load('assets/loh-bg-v2.png').convert_alpha()
hopps_image = pygame.image.load("assets/Hopps.png").convert_alpha()

# create instances
hopps = Hopps(hopps_image, c.HOPPS_START_POS)

run = True
while run:

    ##### DRAW SECTION #####
    screen.blit(background, (0, 0))
    screen.blit(hopps_image, hopps.pos)


    ##### UPDATE SECIONT #####
    hopps.update()

    for event in pygame.event.get():
        # quit program
        if event.type == pygame.QUIT:
            run = False

    clock.tick(c.FPS)
    pygame.display.update()

pygame.quit()
