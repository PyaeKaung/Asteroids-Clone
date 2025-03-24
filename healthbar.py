import pygame as pg

def draw_health_bar(surface, x, y, health, max_health, height=300, width=20):
    healthratio = max(0, health / max_health) 
    border_rect = pg.Rect(x - 2, y - 2, width + 4, height + 4)
    pg.draw.rect(surface, (255, 255, 255), border_rect)
    pg.draw.rect(surface, (0, 0, 0), (x, y, width, height))
    pg.draw.rect(surface, (0, 255, 0), (x, y + height * (1 - healthratio), width, height * healthratio))
