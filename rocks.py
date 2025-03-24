import pygame as pg
import random
import math

asteroidimages = [
    pg.transform.scale(pg.image.load('images/asteroid1.png'), (70, 70)),
    pg.transform.scale(pg.image.load('images/asteroid2.png'), (70, 70)),
    pg.transform.scale(pg.image.load('images/asteroid3.png'), (70, 70))
]

def getrandompos(center, radius):
    while True:
        x = random.uniform(center[0] - radius, center[0] + radius)
        y = random.uniform(center[1] - radius, center[1] + radius)
        if (x - center[0])**2 + (y - center[1])**2 <= radius**2:
            return pg.Vector2(x, y)

class Asteroid:
    def __init__(self, center, radius):
        self.pos = getrandompos(center, radius)
        self.image = random.choice(asteroidimages)
        scale = random.uniform(0.7, 1.5)
        self.image = pg.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.angle = random.uniform(0, 360)
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        self.direction = pg.Vector2(random.uniform(-1, 1), random.uniform(-1,1)).normalize()
        self.speed = random.uniform(2, 5)
        self.rect = self.rotated_image.get_rect(center=self.pos)
        self.hp = random.randint(5, 21)

    def collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    def update(self, worldcenter, world_radius):
        self.pos += self.direction * self.speed
        distance_from_center = self.pos.distance_to(pg.Vector2(worldcenter))
        if distance_from_center > world_radius:
            direction_to_center = (pg.Vector2(worldcenter) - self.pos).normalize()
            self.pos = pg.Vector2(worldcenter) + direction_to_center * world_radius
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_image.get_rect(center=self.pos)

    def draw(self, screen, camx, camy):
        screen.blit(self.rotated_image, (self.pos.x - camx, self.pos.y - camy))

def generate_asteroids(num_asteroids, world_center, world_radius):
    return [Asteroid(world_center, world_radius) for _ in range(num_asteroids)]
