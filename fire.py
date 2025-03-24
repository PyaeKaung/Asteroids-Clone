import pygame as pg
bullet_speed = 30
class Bullet:
    def __init__(self, pos, target_pos):
        self.pos = pg.Vector2(pos)
        direction = pg.Vector2(target_pos) - self.pos
        if direction.length() != 0:
            direction = direction.normalize()
        self.vel = direction * bullet_speed
        self.radius = 5
        self.life = 2000
        self.spawntime = pg.time.get_ticks()
        self.image = pg.Surface((10, 10), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 255, 255), (5, 5), self.radius)
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

    def draw(self, screen, camx, camy):
        screen.blit(self.image, (self.pos.x - camx - 5, self.pos.y - camy - 5))

fire_cooldown = 100
lastshottime = 0
shotsfired = 0
maxshots = 20
reloading = False
reloadstarttime = 0
reloadduration = 3000
