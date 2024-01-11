import pygame as pg
import constants as c

pg.init()

screen = pg.display.set_mode((c.WIDTH, c.HEIGHT))
pg.display.set_caption("Life of Hopps")

# load images

background = pg.image.load('assets/life-of-hopps.png').convert_alpha()
screen.blit(background, (0, 0))

run = True
while run:

    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False

pg.quit()