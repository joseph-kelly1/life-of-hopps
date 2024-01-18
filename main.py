import pygame
from settings import *
import math

# setup pygame

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption("Life of Hopps")
pygame.display.set_icon(pygame.image.load("assets/life-of-hopps-icon.png"))

clock = pygame.time.Clock()

# load images
background = pygame.image.load('assets/loh-bg-v3.png').convert()


class Hopps(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Hopps.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, HOPPS_SCALE)
        self.pos = pygame.math.Vector2(HOPPS_START_POS)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.speed = 8
        self.shoot = False
        self.shoot_cooldown = 0
        self.vel_x = 0
        self.vel_y = 0

    def get_angle(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.mouse_x = (self.mouse_coords[0] - self.rect.centerx)
        self.mouse_y = (self.mouse_coords[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(self.mouse_y, self.mouse_x))

    def user_input(self):

        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel_y = -HOPPS_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel_y = HOPPS_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -HOPPS_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = HOPPS_SPEED

        if not(keys[pygame.K_w] or keys[pygame.K_UP]) and not(keys[pygame.K_s] or keys[pygame.K_DOWN]) and not(keys[pygame.K_a] or keys[pygame.K_LEFT]) and not(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.vel_x = 0
            self.vel_y = 0

        if self.vel_x != 0 and self.vel_y != 0:
            self.vel_x /= math.sqrt(2)
            self.vel_y /= math.sqrt(2)

        # Shooting
        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            spawn_bullet_pos = self.pos
            self.bullet = Bullet(spawn_bullet_pos[0] + (.5 * self.rect.width), spawn_bullet_pos[1] + (.5 * self.rect.height), self.angle)
            bullet_group.add(self.bullet)
            sprites_group.add(self.bullet)

    def move(self):
        self.rect.topleft = self.pos
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)

    def update(self):
        self.move()
        self.user_input()

        self.get_angle()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("assets/dice.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft=(0, 0))

    def custom_draw(self):
        self.offset.x = hopps.rect.centerx - WIDTH // 2
        self.offset.y = hopps.rect.centery - HEIGHT // 2

        # draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        for sprite in sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)


camera = Camera()
hopps = Hopps()


sprites_group = pygame.sprite.Group()
sprites_group.add(hopps)

bullet_group = pygame.sprite.Group()


run = True
while run:

    # pygame.draw.rect(screen, "black", hopps.rect, width=2)

    # screen.blit(background, (0, 0))
    screen.fill((0, 0, 0))

    camera.custom_draw()
    # sprites_group.draw(screen)


    for event in pygame.event.get():
        # quit program
        if event.type == pygame.QUIT:
            run = False

    sprites_group.update()
    hopps.update()

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
