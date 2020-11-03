import pygame as pg
from game_context import *

class Player:
    def __init__(self, x, y, w, h, speed):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.speed = speed

        self.ground = res[1]
        self.yvel = 0
        self.state = "GROUNDED"

    def on_keydown(self, key):
        if (key == pg.K_UP 
            and self.state == "GROUNDED"):
            self.state = "AIRBORNE"
            self.y -= 1
            self.yvel = 1000

    def update(self, platforms, dt):

        belows = [ i
            for i, p_rect in enumerate(platforms)
            if (p_rect.left < self.x + self.w//2)
            and (self.x - self.w//2 < p_rect.right)
            and (
                (p_rect.y >= self.y)
                or (p_rect.ismoving 
                    and (abs(self.ground - p_rect.y) <= V_TH))
                )]

        belows.sort(key=lambda i: platforms[i].y)
        ground_platform_index = belows[0]

        self.ground = platforms[ground_platform_index].y

        if (self.state == "GROUNDED"
            and platforms[ground_platform_index].ismoving):
            self.x += platforms[ground_platform_index].dx
            self.y += platforms[ground_platform_index].dy
        
        keymap = pg.key.get_pressed()

        dx = 0
        if keymap[pg.K_RIGHT]:
            dx = self.speed * dt
        if keymap[pg.K_LEFT]:
            dx = -1 * self.speed * dt
        if self.state == "AIRBORNE":
            dx *= 1.3

        self.x += dx
        if (self.x - self.w//2) < 0:
            self.x = self.w//2
        elif (self.x + self.w//2) > res[0]:
            self.x = res[0] - self.w//2

        if self.y < self.ground:
            self.state = "AIRBORNE"
            self.yvel += G_CONST
            dy = -1 * self.yvel * dt
            self.y += dy
            if self.y > self.ground:
                self.y = self.ground
        else:
            self.state = "GROUNDED"
            self.yvel = 0
            self.y = self.ground


    def draw(self, surf):
        pg.draw.rect( surf, WHITE if self.state== "AIRBORNE" else GREEN, 
            pg.Rect(    int(self.x - self.w//2),
                        int(self.y - self.h),
                        self.w,self.h), 1)