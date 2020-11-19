import pygame as pg
from game_context import *

import pygame as pg
from game_context import *

class Trophy:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h

        self.hitbox = pg.Rect(
            self.x - 3* self.w//2, 
            self.y - self.h,
            self.w*3, self.h)

    def draw(self, surf):
        pg.draw.rect( surf, YELLOW, 
            pg.Rect(    int(self.x - self.w//2),
                        int(self.y - self.h),
                        self.w, self.h), 1)

        pg.draw.rect( surf, RED, self.hitbox, 1)