import pygame as pg

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image,(width * scale, height * scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == True and self.clicked == False:
                self.clicked = True
                action = True
        if pg.mouse.get_pressed()[0] == False:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action