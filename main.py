import pygame
import constants as c
import math

# setup pygame

pygame.init()

screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Life of Hopps")

clock = pygame.time.Clock()

# load images
background = pygame.image.load('assets/loh-bg-v2.png').convert_alpha()


class Hopps(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Hopps.png").convert_alpha()
        self.pos = pygame.math.Vector2(c.HOPPS_START_POS)
        # self.rect = self.image.get_rect(center=self.pos)
        self.speed = 8

    def user_input(self):
        self.vel_x = 0
        self.vel_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel_y = -c.HOPPS_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel_y = c.HOPPS_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -c.HOPPS_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = c.HOPPS_SPEED

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.vel_y = 0
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.vel_x = 0

        if self.vel_x != 0 and self.vel_y != 0:
            self.vel_x /= math.sqrt(2)
            self.vel_y /= math.sqrt(2)

    def move(self):
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
    def update(self):
        self.user_input()
        self.move()


hopps = Hopps()


run = True
while run:

    screen.blit(background, (0, 0))

    screen.blit(hopps.image, hopps.pos)
    hopps.update()

    for event in pygame.event.get():
        # quit program
        if event.type == pygame.QUIT:
            run = False

    clock.tick(c.FPS)
    pygame.display.update()

pygame.quit()
