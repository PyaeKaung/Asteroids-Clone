import random
import pygame as pg

class Particle:
    def __init__ (self, pos):
        self.x, self.y = pos
        self.size = random.randint(10,15)
        self.color = (255, 127, 0)
        self.life = random.randint(30,40)
        self.vx = random.uniform(-5, -2)
        self.vy = random.uniform(-5, -2)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface, camx, camy):
        if self.life > 0:
            rect = pg.Rect(int(self.x - camx - -5), int(self.y - camy - 0), self.size, self.size)
            pg.draw.rect(surface, self.color, rect)