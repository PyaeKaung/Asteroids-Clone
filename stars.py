import random
import pygame as pg

world_radius = 6000

def getrandompos(center, radius):
    while True:
        x = random.uniform(center[0] - radius, center[0] + radius)
        y = random.uniform(center[1] - radius, center[1] + radius)

        if (x - center[0])**2 + (y - center[1])**2 <= radius**2:
            return pg.Vector2(x, y)


spawnlimit = random.randint(200,300)
worldcenter = (world_radius, world_radius)

star = pg.transform.scale(pg.image.load('images/star.png'), (30, 30))

spawn_points = [getrandompos(worldcenter, world_radius) for _ in range(spawnlimit)]