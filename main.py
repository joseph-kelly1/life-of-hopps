import pygame
import sys
from settings import *
from levels import *
import math
import random

# setup pygame

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h - 100

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption("Life of Hopps")
pygame.display.set_icon(pygame.image.load("assets/life-of-hopps-icon.png"))

clock = pygame.time.Clock()

# load images
background = pygame.image.load('assets/loh-bg-v4.png').convert_alpha()
ui_bar = pygame.image.load('assets/loh-ui-bar.png').convert_alpha()
title_sheet = pygame.image.load('assets/loh_title-Sheet.png').convert_alpha()
pause_icon = pygame.image.load('assets/pause.png').convert_alpha()
pause_icon = pygame.transform.rotozoom(pause_icon, 0, 1.4)

spider_image = pygame.image.load('assets/spider.png').convert_alpha()
beetle_image = pygame.image.load('assets/beetle.png').convert_alpha()
stinkbug_image = pygame.image.load('assets/stinkbug.png').convert_alpha()

# load hopps spritesheet
all_hopps = pygame.image.load("assets/All_Hopps.png").convert_alpha()

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


# function for getting sprite sheet frames
def get_frames(sheet, frame_width, frame_height):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            frame = sheet.subsurface((x, y, frame_width, frame_height))
            frames.append(frame)
    return frames


# FONTS
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


TEXT_COLOR = (255, 255, 255)


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
        self.regen_timer = 300

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

        if not (keys[pygame.K_w] or keys[pygame.K_UP]) and not (keys[pygame.K_s] or keys[pygame.K_DOWN]) and not (
                keys[pygame.K_a] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
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
        if ((keys[pygame.K_w] or keys[pygame.K_UP]) and hopps.pos[1] <= 9) \
                or ((keys[pygame.K_s] or keys[pygame.K_DOWN]) and hopps.pos[
            1] >= background.get_height() - hopps.image.get_height()):
            self.vel_y = 0

        if ((keys[pygame.K_a] or keys[pygame.K_LEFT]) and hopps.pos[0] <= -9) \
                or ((keys[pygame.K_d] or keys[pygame.K_RIGHT]) and hopps.pos[
            0] >= background.get_width() - hopps.image.get_width() + 9):
            self.vel_x = 0

        # Shooting
        self.get_angle()
        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False


    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            spawn_bullet_pos = self.pos
            self.bullet = Bullet(spawn_bullet_pos[0] + (.5 * self.rect.width),
                                 spawn_bullet_pos[1] + (.5 * self.rect.height), self.angle)
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

        if health_bar.hp > 0:
            if health_bar.hp < 100 and self.regen_timer > 0:
                self.regen_timer -= 1

            if self.regen_timer == 0:
                health_bar.hp += 5
                self.regen_timer = 300

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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, image):
        super().__init__(enemy_group, sprites_group)
        self.position = pygame.math.Vector2(position)
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.acc = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        self.collide = False
        self.health = 5
        self.alive = True
        self.attack_timer = 0

    def hunt_player(self, player):
        player_vector = pygame.math.Vector2(player.rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)

        # Check if the enemy and player positions are not the same
        if player_vector != enemy_vector:
            direction = (player_vector - enemy_vector).normalize()
            self.velocity = direction * self.speed
            self.acc += self.velocity
            if self.acc[0] >= 10:
                self.acc[0] = 10
            if self.acc[1] >= 10:
                self.acc[1] = 10
            self.position += self.velocity
            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y

            # angle enemy toward hopps
            x = self.rect.x - hopps.rect.x
            y = self.rect.y - hopps.rect.y
            self.angle = math.degrees(math.atan2(x, y))
            self.image = pygame.transform.rotate(self.original_image, self.angle)

    def check_collision(self):
        # Inside your game loop:
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if pygame.sprite.collide_rect(hopps, self) and self.attack_timer == 0 and health_bar.hp > 0:
            health_bar.hp -= 10
            self.attack_timer = 60


        for bullet in bullet_group:
            if pygame.sprite.collide_rect(bullet, self):  # Check collision
                self.health -= dice_level  # Reduce enemy health
                bullet.bullet_lifetime = 0  # Remove the bullet

    def check_alive(self):
        global dice_level_bar
        if self.health <= 0:
            self.kill()
            if not(total_level_enemies %2 == 0):
                dice_level_bar.hp += (100/total_level_enemies + 1)
            else:
                dice_level_bar.hp += (100/total_level_enemies)


    def get_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def update(self):
        self.hunt_player(hopps)
        self.check_collision()
        self.check_alive()


class HealthBar():
    def __init__(self, x, y, w, h, max_hp, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
        self.color = color

    def draw(self, surface):
        # calculate health ratio
        if self.hp > 100:
            self.hp = 100
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "grey", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.w * ratio, self.h))
        pygame.draw.rect(surface, "black", (self.x, self.y, self.w, self.h), width=5)


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


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


sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

camera = Camera()
hopps = Hopps()
health_bar = HealthBar(20, 20, 300, 40, 100, "red")
health_bar.hp = 100
dice_level_bar = HealthBar(1020, 20, 300, 40, 100, "green")
dice_level_bar.hp = 0
dice_level = 1
level = 1
total_level_enemies = 0

sprites_group.add(hopps)


def loadlevel(level):
    global total_level_enemies
    current_level = levels[level-1]

    for i in range(current_level["spiders"]):
        spider = Enemy((random.randint(0, 2048),random.randint(0, 1408)), spider_image)
        sprites_group.add(spider)
        enemy_group.add(spider)
        total_level_enemies += 1
    for i in range(current_level["beetles"]):
        beetle = Enemy((random.randint(0, 2048),random.randint(0, 1408)), beetle_image)
        sprites_group.add(beetle)
        enemy_group.add(beetle)
        total_level_enemies += 1
    for i in range(current_level["stinkbugs"]):
        stinkbug = Enemy((random.randint(0, 2048),random.randint(0, 1408)), stinkbug_image)
        sprites_group.add(stinkbug)
        enemy_group.add(stinkbug)
        total_level_enemies += 1

    print(total_level_enemies)

loadlevel(level)



def restart():
    global camera, hopps, sprites_group, level, dice_level, dice_level_bar, total_level_enemies
    hopps = Hopps()
    hopps.shoot_cooldown = 80
    health_bar.hp = 100
    dice_level = 1
    dice_level_bar.hp = 0
    total_level_enemies = 0

    camera = Camera()

    sprites_group.empty()
    enemy_group.empty()
    sprites_group.add(hopps)
    level = 1
    loadlevel(level)



def menu():
    title_speed = pygame.time.Clock()

    frames = get_frames(title_sheet, title_sheet.get_width(), 128)
    frame_index = 0
    frame_count = len(frames)
    count = 0

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        hopps.shoot_cooldown = 80

        screen.fill((135, 206, 235))

        current_frame = frames[frame_index]
        screen.blit(current_frame, ((title_sheet.get_width() - WIDTH) / -2, 100))  # Adjust position as needed

        play_button = Button(None, pos=((WIDTH / 2), 380),
                             text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        controls_button = Button(None, pos=((WIDTH / 2), 530),
                                 text_input="Controls", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        exit_button = Button(None, pos=((WIDTH / 2), 680),
                             text_input="Exit", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        controls_button.changeColor(MENU_MOUSE_POS)
        controls_button.update(screen)

        play_button.changeColor(MENU_MOUSE_POS)
        play_button.update(screen)

        exit_button.changeColor(MENU_MOUSE_POS)
        exit_button.update(screen)

        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(MENU_MOUSE_POS):
                    restart()
                    run()
                    hopps.shoot_cooldown = 0
                if controls_button.checkForInput(MENU_MOUSE_POS):
                    menu_controls()
                if exit_button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()


        title_speed.tick(60)
        pygame.display.flip()

        count += 1
        if count == 3:
            frame_index = (frame_index + 1) % frame_count
            count = 0


def run():
    global level
    global dice_level
    global dice_level_bar

    while True:
        RUN_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill((0, 0, 0))

        camera.custom_draw()
        screen.blit(ui_bar, ((2048 - WIDTH) / -2, 0))

        health_bar.draw(screen)
        draw_text("Level: " + str(level), get_font(25), "black", 20, 80)
        dice_level_bar.draw(screen)
        draw_text("Dice Level:" + str(dice_level), get_font(25), "black", 1020, 80)




        pause_button = Button(pause_icon, pos=(WIDTH-60, 60),
                             text_input="", font=get_font(20), base_color="black", hovering_color="#d7fcd4")

        pause_button.update(screen)

        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                if event.key == pygame.K_r:
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.checkForInput(RUN_MOUSE_POS):
                    pause()

        if not enemy_group:
            level += 1
            if level <= 10:
                loadlevel(level)

        if dice_level_bar.hp == 100 and dice_level < 5:
            dice_level += 1
            if dice_level < 5:
                dice_level_bar.hp = 0

        sprites_group.update()
        hopps.update()

        clock.tick(FPS)
        pygame.display.update()

        if health_bar.hp <= 0:
            game_over()


def pause():
    overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 128))

    while True:

        PAUSE_MOUSE_POS = pygame.mouse.get_pos()
        hopps.shoot_cooldown = 100

        screen.fill((0, 0, 0))
        camera.custom_draw()

        screen.blit(overlay_surface, (0, 0))

        pygame.draw.rect(screen, (135, 206, 235), (200, 150, WIDTH - 400, HEIGHT - 300))

        paused_text = Button(None, pos=((WIDTH / 2), 240),
                             text_input="PAUSED", font=get_font(75), base_color="White", hovering_color="White")

        resume_button = Button(None, pos=((WIDTH / 2), 370),
                               text_input="Resume", font=get_font(35), base_color="White", hovering_color="#d7fcd4")

        restart_button = Button(None, pos=((WIDTH / 2), 450),
                                text_input="Menu", font=get_font(35), base_color="White", hovering_color="#d7fcd4")

        controls_button = Button(None, pos=((WIDTH / 2), 520),
                                 text_input="Controls", font=get_font(35), base_color="White", hovering_color="#d7fcd4")

        paused_text.update(screen)

        resume_button.changeColor(PAUSE_MOUSE_POS)
        resume_button.update(screen)

        restart_button.changeColor(PAUSE_MOUSE_POS)
        restart_button.update(screen)

        controls_button.changeColor(PAUSE_MOUSE_POS)
        controls_button.update(screen)

        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run()
                    hopps.shoot_cooldown = 0
                if event.key == pygame.K_r:
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.checkForInput(PAUSE_MOUSE_POS):
                    run()
                    hopps.shoot_cooldown = 0
                if restart_button.checkForInput(PAUSE_MOUSE_POS):
                    menu()
                if controls_button.checkForInput(PAUSE_MOUSE_POS):
                    from_pause = True
                    pause_controls()

        clock.tick(FPS)
        pygame.display.update()


def pause_controls():
    overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 128))

    while True:

        CONTROLS_MOUSE_POS = pygame.mouse.get_pos()
        hopps.shoot_cooldown = 100

        screen.fill((0, 0, 0))
        camera.custom_draw()

        screen.blit(overlay_surface, (0, 0))

        pygame.draw.rect(screen, (135, 206, 235), (200, 150, WIDTH - 400, HEIGHT - 300))

        controls_text = Button(None, pos=((WIDTH / 2), 220),
                               text_input="Controls", font=get_font(75), base_color="White", hovering_color="White")

        movement_text = Button(None, pos=((WIDTH / 2), 340),
                               text_input="WASD or Arrow Keys to Move", font=get_font(30), base_color="White",
                               hovering_color="#d7fcd4")

        shooting_text = Button(None, pos=((WIDTH / 2), 420),
                               text_input="LMB or Space to Shoot", font=get_font(30), base_color="White",
                               hovering_color="#d7fcd4")

        back_button = Button(None, pos=((WIDTH / 2) - 200, 540),
                             text_input="Back", font=get_font(40), base_color="White", hovering_color="#d7fcd4")

        restart_button = Button(None, pos=((WIDTH / 2) + 200, 540),
                                text_input="Menu", font=get_font(40), base_color="White", hovering_color="#d7fcd4")

        controls_text.update(screen)

        movement_text.update(screen)

        shooting_text.update(screen)

        restart_button.changeColor(CONTROLS_MOUSE_POS)
        restart_button.update(screen)

        back_button.changeColor(CONTROLS_MOUSE_POS)
        back_button.update(screen)

        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run()
                    hopps.shoot_cooldown = 0
                if event.key == pygame.K_r:
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(CONTROLS_MOUSE_POS):
                    pause()
                    hopps.shoot_cooldown = 0
                if restart_button.checkForInput(CONTROLS_MOUSE_POS):
                    menu()

        clock.tick(FPS)
        pygame.display.update()


def menu_controls():
    overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay_surface.fill((0, 0, 0, 128))

    while True:

        CONTROLS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill((135, 206, 235))
        screen.blit(overlay_surface, (0, 0))

        pygame.draw.rect(screen, (135, 206, 235), (200, 150, WIDTH - 400, HEIGHT - 300))

        controls_text = Button(None, pos=((WIDTH / 2), 220),
                               text_input="Controls", font=get_font(75), base_color="White", hovering_color="White")

        movement_text = Button(None, pos=((WIDTH / 2), 340),
                               text_input="WASD or Arrow Keys to Move", font=get_font(30), base_color="White",
                               hovering_color="#d7fcd4")

        shooting_text = Button(None, pos=((WIDTH / 2), 420),
                               text_input="LMB or Space to Shoot", font=get_font(30), base_color="White",
                               hovering_color="#d7fcd4")

        back_button = Button(None, pos=((WIDTH / 2), 540),
                             text_input="Back", font=get_font(40), base_color="White", hovering_color="#d7fcd4")

        controls_text.update(screen)

        movement_text.update(screen)

        shooting_text.update(screen)

        back_button.changeColor(CONTROLS_MOUSE_POS)
        back_button.update(screen)

        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run()
                    hopps.shoot_cooldown = 0
                if event.key == pygame.K_r:
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.checkForInput(CONTROLS_MOUSE_POS):
                    menu()

        clock.tick(FPS)
        pygame.display.update()


def game_over():

    while True:
        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        game_over_text = Button(None, pos=((WIDTH / 2), 250),
                             text_input="Game Over", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        score_text = Button(None, pos=((WIDTH / 2), 400),
                             text_input="Score:1000", font=get_font(60), base_color="White", hovering_color="#d7fcd4")

        menu_button = Button(None, pos=((WIDTH / 2)-200, 540),
                                text_input="Menu", font=get_font(40), base_color="White", hovering_color="#d7fcd4")

        exit_button = Button(None, pos=((WIDTH / 2)+200, 540),
                                text_input="Exit", font=get_font(40), base_color="White", hovering_color="#d7fcd4")

        game_over_text.update(screen)

        score_text.update(screen)

        menu_button.changeColor(GAME_OVER_MOUSE_POS)
        menu_button.update(screen)

        exit_button.changeColor(GAME_OVER_MOUSE_POS)
        exit_button.update(screen)

        for event in pygame.event.get():
            # quit program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.checkForInput(GAME_OVER_MOUSE_POS):
                    menu()
                if exit_button.checkForInput(GAME_OVER_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)
        pygame.display.update()


menu()


pygame.quit()
