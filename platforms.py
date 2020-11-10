import pygame as pg
from game_context import *

class Platform(pg.Rect):
    def __init__(self, x, y, w, h):
        pg.Rect.__init__(self, x, y, w, h)
        self.ismoving = False
 
    def update(self, dt):
        pass

    def draw(self, surf):
        pg.draw.rect(surf, BLUE, self, 1)

import math
class BackForthMovingPlatform(Platform):
    def __init__(self, x, y, w, h, L, R, hspeed, T, B, vspeed):
        Platform.__init__(self, x, y, w, h)
        self.center_x, self.center_y = (L + R)/2, (T + B)/2
        self.x = self.center_x - self.w/2
        self.y = self.center_y - self.h/2
        self.time = 0
        self.L, self.R, self.T, self.B = L, R, T, B
        self.hspeed, self.vspeed = hspeed, vspeed
        self.ismoving = True
        self.prev_x, self.prev_y = self.center_x, self.center_y
        self.dx, self.dy = 0, 0

    def update(self, dt):
        self.time += dt
        self.x = self.center_x + (self.R - self.L - self.w)/2 * math.sin(self.hspeed * self.time) - self.w/2
        self.y = self.center_y + (self.T - self.B)/2 * math.sin(self.vspeed * self.time)

        self.dx = self.x - self.prev_x
        self.dy = self.y - self.prev_y

        self.prev_x = self.x
        self.prev_y = self.y

class CircleMovingPlatform(Platform):
    def __init__(self, x, y, w, h, L, R, hspeed, T, B, vspeed):
        Platform.__init__(self, x, y, w, h)
        self.center_x, self.center_y = (L + R)/2, (T + B)/2
        self.x = self.center_x - self.w/2
        self.y = self.center_y - self.h/2
        self.time = 0
        self.L, self.R, self.T, self.B = L, R, T, B
        self.hspeed, self.vspeed = hspeed, vspeed
        self.ismoving = True
        self.prev_x, self.prev_y = self.center_x, self.center_y
        self.dx, self.dy = 0, 0

    def update(self, dt):
        self.time += dt
        self.x = self.center_x + (self.R - self.L - self.w)/2 * math.sin(self.hspeed * self.time) - self.w/2
        self.y = self.center_y + (self.T - self.B)/2 * math.cos(self.vspeed * self.time)

        self.dx = self.x - self.prev_x
        self.dy = self.y - self.prev_y

        self.prev_x = self.x
        self.prev_y = self.y

class Platforms(list):
    def __init__(self, platforms_path):
        list.__init__(self)
        self.append(Platform(0, res[1], res[0], 0))
        
        self.platforms_path = platforms_path
        self.stationary_canvas = pg.Surface(res)
        self.init_platforms()


    def init_platforms(self):
        with open(self.platforms_path, "r") as f__:
            for line in f__.read().split('\n'):
                raws = [float(num) for num in line.split(",")]
                platform_type, platform_data = raws[0], raws[1:]

                if platform_type == NPLAT:
                    self.append(Platform(*platform_data))
                elif platform_type == BPLAT:
                    self.append(BackForthMovingPlatform(*platform_data))
                elif platform_type == CPLAT:
                    self.append(CircleMovingPlatform(*platform_data))

        self.static_platforms = [ p for p in self[1:] if not p.ismoving ]
        for p in self.static_platforms:
            p.draw(self.stationary_canvas)
        self.dynamic_platforms = [ p for p in self[1:] if p.ismoving ]

    def update(self, dt):
        for x in self.dynamic_platforms:
            x.update(dt)

    def draw(self, surf):
        surf.blit(self.stationary_canvas,(0,0))
        for x in self.dynamic_platforms:
            x.draw(surf)
