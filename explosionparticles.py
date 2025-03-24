import pygame as pg
import random

class ExplosionParticle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.size = random.randint(10,15)
        self.color = (255, 127, 0)
        self.life = random.randint(30,40)
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface, camx, camy):
        if self.life > 0:
            rect = pg.Rect(int(self.x - camx), int(self.y - camy), self.size, self.size)
            pg.draw.rect(surface, self.color, rect)
