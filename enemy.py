import pygame as pg
import math, random

class EnemyBullet:
    def __init__(self, pos, player_pos, fire_sound):
        self.pos = pg.Vector2(pos)
        direction = (player_pos - self.pos)
        if direction.length() != 0:
            direction = direction.normalize() * 20
        self.velocity = direction
        self.life = 3000
        self.spawn_time = pg.time.get_ticks()
        self.radius = 5
        self.rect = pg.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)
        pg.mixer.Channel(3).play(fire_sound)
    def collision(self, player_rect):
        return self.rect.colliderect(player_rect)


    def update(self):
        self.pos += self.velocity
        self.rect.topleft = (self.pos.x - self.radius, self.pos.y - self.radius)
        return pg.time.get_ticks() - self.spawn_time <= self.life

    def draw(self, screen, camx, camy):
        pg.draw.circle(screen, (0, 255, 0), (int(self.pos.x - camx), int(self.pos.y - camy)), self.radius)


class Enemy:
    def __init__(self, player, bullet_list, image, fire_sound):
        self.player = player
        self.bullet_list = bullet_list
        self.image = image
        self.fire_sound = fire_sound
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 1000)
        self.pos = self.player.player_pos + pg.Vector2(math.cos(angle), math.sin(angle)) * radius
        self.velocity = pg.Vector2(0, 0)
        self.acceleration = 1
        self.max_speed = 12
        self.target_point = None
        self.last_fire_time = pg.time.get_ticks()
        self.pick_new_target()

    def get_rect(self, camx=0, camy=0):
        return self.image.get_rect(center= (self.pos.x - camx, self.pos.y - camy))

    def pick_new_target(self):
        current_time = pg.time.get_ticks() / 1000
        rotation_speed = 30
        base_angles = [0, 90, 180, 270]
        chosen_angle_deg = random.choice(base_angles)
        total_angle_deg = chosen_angle_deg + rotation_speed * current_time
        total_angle_rad = math.radians(total_angle_deg)
        offset = pg.Vector2(math.cos(total_angle_rad), math.sin(total_angle_rad)) * 500
        self.target_point = self.player.player_pos + offset

    def update(self, volume_value=0.7):
        desired = self.target_point - self.pos
        if desired.length() > 0:
            desired = desired.normalize() * self.max_speed
        steer = desired - self.velocity
        if steer.length() > self.acceleration:
            steer.scale_to_length(self.acceleration)
        self.velocity += steer
        self.pos += self.velocity

        if self.pos.distance_to(self.target_point) < 10:
            current_time = pg.time.get_ticks()
            if current_time - self.last_fire_time >= 3000:
                self.last_fire_time = current_time
                self.bullet_list.append(EnemyBullet(self.pos, self.player.player_pos, self.fire_sound))
            self.pick_new_target()

    def draw(self, screen, camx, camy):
        rect = self.image.get_rect(center=(int(self.pos.x - camx), int(self.pos.y - camy)))
        screen.blit(self.image, rect)
