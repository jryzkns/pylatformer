# PYGAME BOILERPLATE CODE
# JRYZKNS 2019

import pygame as pg
from game_context import *
from player import Player
from platforms import Platforms
from trophy import Trophy

pg.init()
game_win = pg.display.set_mode(res)

running, paused, dt = True, False, 0
game_clock = pg.time.Clock()
game_clock.tick()

player    = Player(100, 300, 5, 15, 150)
trophy    = Trophy(470, 80, 15, 45)
platforms = Platforms('lvl1.platforms')

player.target = trophy

while running:

    # CALLBACKS
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            player.on_keydown(event.key)
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_d:
                print()

    dt = game_clock.get_time()/1000.

    if not paused:
        platforms .update(dt)
        player    .update(platforms, dt)
  
    # draws
    game_win.fill(BLACK)

    platforms .draw(game_win)
    player    .draw(game_win)
    trophy    .draw(game_win)

    pg.display.flip()
    game_clock.tick()
