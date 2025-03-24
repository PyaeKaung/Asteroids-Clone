import pygame as pg

player_health = 200
max_health = 200
player_speed_increase = 1
player_speed_decrease = 0.1
player_speed = 0
forward_player_max_speed = 10
backward_player_max_speed = -5
player_rotation_speed = 3
player_angle = 0

world_radius = 6000
player_pos = pg.Vector2(world_radius // 2 , world_radius // 2)

player_first_instance = pg.Surface((100, 300), pg.SRCALPHA)
rotated_player = player_first_instance
