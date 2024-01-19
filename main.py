import pygame
from settings import *
import math

# setup pygame

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h - 100

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption("Life of Hopps")
pygame.display.set_icon(pygame.image.load("assets/life-of-hopps-icon.png"))

clock = pygame.time.Clock()

# load images
background = pygame.image.load('assets/loh-bg-v3.png').convert()

# load hopps spritesheet
#player images
all_hopps = pygame.image.load("assets/All_Hopps.png")

sprite_width, sprite_height = 64, 64

player_sprites = {
    "UP_RIGHT_HOPPS": None,
    "UP_LEFT_HOPPS": None,
    "DOWN_RIGHT_HOPPS": None,
    "DOWN_LEFT_HOPPS": None,
    "UP_HOPPS": None,
    "DOWN_HOPPS": None,
    "RIGHT_HOPPS": None,
    "LEFT_HOPPS": None,
}

for row in range(2):
    for col in range(4):
        x = col * sprite_width
        y = row * sprite_height
        sprite_rect = pygame.Rect(x, y, sprite_width, sprite_height)
        key = list(player_sprites.keys())[len(player_sprites) - (row * 4 + col + 1)]
        new_sprite = pygame.transform.rotozoom(all_hopps.subsurface(sprite_rect).convert_alpha(), 0, HOPPS_SCALE)
        player_sprites[key] = new_sprite


class Hopps(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/Hopps.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, HOPPS_SCALE)
        self.pos = pygame.math.Vector2(HOPPS_START_POS)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.speed = HOPPS_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.vel_x = 0
        self.vel_y = 0

    def get_angle(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.mouse_x = (self.mouse_coords[0] - WIDTH // 2)
        self.mouse_y = (self.mouse_coords[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(self.mouse_y, self.mouse_x))

    def user_input(self):

        keys = pygame.key.get_pressed()

        # movement input
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel_y = -HOPPS_SPEED
            self.image = player_sprites["UP_HOPPS"]
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel_y = HOPPS_SPEED
            self.image = player_sprites["DOWN_HOPPS"]
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -HOPPS_SPEED
            self.image = player_sprites["LEFT_HOPPS"]
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = HOPPS_SPEED
            self.image = player_sprites["RIGHT_HOPPS"]

        if not(keys[pygame.K_w] or keys[pygame.K_UP]) and not(keys[pygame.K_s] or keys[pygame.K_DOWN]) and not(keys[pygame.K_a] or keys[pygame.K_LEFT]) and not(keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.vel_x = 0
            self.vel_y = 0

        if self.vel_x != 0 and self.vel_y != 0:
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                self.image = player_sprites["UP_LEFT_HOPPS"]
            if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                self.image = player_sprites["UP_RIGHT_HOPPS"]
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
                self.image = player_sprites["DOWN_LEFT_HOPPS"]
            if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
                self.image = player_sprites["DOWN_RIGHT_HOPPS"]

            self.vel_x /= math.sqrt(2)
            self.vel_y /= math.sqrt(2)

        # boundaries
        if ((keys[pygame.K_w] or keys[pygame.K_UP]) and hopps.pos[1] <= 90) \
                or ((keys[pygame.K_s] or keys[pygame.K_DOWN]) and hopps.pos[1] >= background.get_height() - hopps.image.get_height()):
            self.vel_y = 0

        if ((keys[pygame.K_a] or keys[pygame.K_LEFT]) and hopps.pos[0] <= -9) \
                or ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) and hopps.pos[0] >= background.get_width() - hopps.image.get_width() + 9):
            self.vel_x = 0

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
        self.speed = BULLET_SPEED
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
