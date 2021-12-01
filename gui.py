from typing import *
import pygame as pg;
from maze import Maze;
import style;
from maze_display import pre_render as render_maze;

DIM = (30, 20);
FENSTER = ((style.S_FELD + style.S_WAND) * DIM[0] + style.S_WAND, (style.S_FELD + style.S_WAND) * DIM[1] + style.S_WAND);

YAMMIE = pg.transform.smoothscale(pg.image.load("yammie.png"), (min(*FENSTER), min(*FENSTER)));

screen = pg.display.set_mode((FENSTER[0], FENSTER[1] + style.S_FOOT));
uhr = pg.time.Clock();
weiter = True;
gegessen = [];

maze = Maze(DIM[0], DIM[1], True);
STEIN = list(maze.entry);
maze.create_food(10);

render_count = 0;

def render ():
    render_maze(screen, maze, STEIN);

    font = pg.font.SysFont("times", int(style.S_FOOT * 0.75));
    text = font.render(f"  Pos: {STEIN[0]}x{STEIN[1]}    Food: {len(gegessen)}/{len(gegessen) + len(maze.food)}", True, "#eeeeee", "#444444");
    pg.draw.rect(screen, "#444444", (0, FENSTER[1], FENSTER[0], style.S_FOOT));
    screen.blit(text, (0, FENSTER[1] + style.S_FOOT * 0.125))

    pg.display.flip();

pg.init();
render();

while weiter:
    uhr.tick(40)
    for e in pg.event.get():
        if (e.type == pg.QUIT): weiter = False;
        elif (e.type == pg.KEYDOWN):
            if (e.key < 1073741907 and e.key > 1073741902):     # PFEILTASTE
                w = maze.walls(*STEIN);
                if (e.key == pg.K_UP and not w[0]): STEIN[1] -= 1;
                elif (e.key == pg.K_RIGHT and not w[1]): STEIN[0] += 1;
                elif (e.key == pg.K_DOWN and not w[2]): STEIN[1] += 1;
                elif (e.key == pg.K_LEFT and not w[3]): STEIN[0] -= 1;
                if (tuple(STEIN) in maze.food):
                    gegessen.append(maze.food.pop(maze.food.index(tuple(STEIN))));
                    screen.fill(style.F_FOOD);
                    screen.blit(YAMMIE, ((FENSTER[0] - min(*FENSTER)) / 2, (FENSTER[1] - min(*FENSTER)) / 2))
                    pg.display.flip();
                    pg.time.wait(400);
            elif (e.key == pg.K_0): STEIN = maze.entry;
            render();
        else: continue;
            

pg.quit()
