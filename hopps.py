import pygame as pg

class Hopps:
    def __int__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y


