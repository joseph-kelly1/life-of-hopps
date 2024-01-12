import pygame
import math
import constants as c

class Hopps:
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos
        self.vel_x = 0
        self.vel_y = 0

    def move(self):
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