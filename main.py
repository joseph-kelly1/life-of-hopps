import pygame as pg
import constants as c
from hopps import Hopps

# setup pygame

pg.init()

screen = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption("Life of Hopps")

clock = pg.time.Clock()

# load images
background = pg.image.load('assets/loh-bg-v2.png').convert_alpha()

run = True
while run:

    screen.blit(background, (0, 0))

    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False

    clock.tick(c.FPS)
    pg.display.update()

pg.quit()
