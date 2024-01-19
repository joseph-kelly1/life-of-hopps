import pygame
import math
import constants as c

class Hopps:
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect
        self.rext = self.hitbox_rect.copy()
        self.pos = pos

    def player_rotation(self):
        pass

    def move(self):
        self.vel_x = 0
        self.vel_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.vel_y = -c.HOPPS_SPEED
        if keys[pygame.K_s]:
            self.vel_y = c.HOPPS_SPEED
        if keys[pygame.K_a]:
            self.vel_x = -c.HOPPS_SPEED
        if keys[pygame.K_d]:
            self.vel_x = c.HOPPS_SPEED

        if self.vel_x != 0 and self.vel_y !=0:
            self.vel_x /= math.sqrt(2)
            self.vel_y /= math.sqrt(2)

        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)

    def update(self):
        self.move()
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
