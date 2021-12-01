from typing import *
import pygame as pg
from pygame import surface;
from maze import Maze as Model;
from maze_display import Maze;
import style;

DIM = (10, 10);
FOOD_COUNT = 1;

render_count = 0;
dir_helper = (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT);

TEXT = "";
def update_std_text ():
    global TEXT;
    TEXT = f'  {maze.stein[0]}x{maze.stein[1]}   {len(maze.gegessen)}/{len(maze.gegessen) + len(maze.model.food)}    {steps} Steps';

def yammie ():
    SCREEN.fill(style.F_FOOD);
    SCREEN.blit(YAMMIE, ((FENSTER[0] - min(*FENSTER)) / 2, (FENSTER[1] - min(*FENSTER)) / 2));
    pg.display.flip();
    pg.time.wait(400);

def render ():
    global render_count;
    render_count += 1;
    # print("RENDER #" + str(render_count));
    SCREEN.blit(maze.render(), (0, 0));
    font = pg.font.SysFont("times", int(style.S_FOOT * 0.75));
    text = font.render(TEXT, True, "#eeeeee", "#444444");
    pg.draw.rect(SCREEN, "#444444", (0, FENSTER[1] - style.S_FOOT, FENSTER[0], style.S_FOOT));
    SCREEN.blit(text, (0, FENSTER[1] - (style.S_FOOT * 0.9)))

    pg.display.flip();

def format_input(newdim, cursor):
    return f' Neu: {newdim[0]}{"_" if not cursor else ""} x {(newdim[1] + "_") if cursor else ""}';

def input_new ():
    newdim = ["", ""];
    cursor = 0;
    global TEXT;
    TEXT = format_input(newdim, cursor);
    render();
    weiter = True;
    while weiter:
        uhr.tick(40);
        for e in pg.event.get():
            if (e.type == pg.KEYDOWN):
                if (e.key == pg.K_ESCAPE): weiter = False;
                elif (e.key == pg.K_RETURN):
                    if (newdim[cursor]):
                        cursor += 1;
                        weiter = cursor == 1;
                        TEXT = format_input(newdim, cursor); render();
                    else:
                        TEXT = "EINGABE BITTE!"; render();
                        pg.time.wait(1000);
                        TEXT = format_input(newdim, cursor); render();
                elif (e.key in range(48, 58)):
                    newdim[cursor] += str(e.key - 48);
                    TEXT = format_input(newdim, cursor); render();
    if (cursor == 2):
        init(int(newdim[0]), int(newdim[1]));
    else: #Wurde abgbrochen
        update_std_text();
        render();

def init(x: int, y: int):
    global maze, FENSTER, SCREEN, uhr, steps, YAMMIE;
    maze = Maze(Model(x, y, True));
    maze.model.mkfood(FOOD_COUNT);
    FENSTER = (maze.grössen[0], maze.grössen[1] + style.S_FOOT);
    SCREEN = pg.display.set_mode(FENSTER);
    pg.display.set_caption(f'Maze {x} x {y}');
    uhr = pg.time.Clock();
    steps = 0;
    YAMMIE = pg.transform.smoothscale(pg.image.load("yammie.png"), (min(*FENSTER), min(*FENSTER)));
    update_std_text();
    render();

pg.init();
init(*DIM);

weiter = True;
while weiter:
    uhr.tick(40)
    for e in pg.event.get():
        if (e.type == pg.QUIT): weiter = False;
        elif (e.type == pg.KEYDOWN):
            if (e.key in dir_helper):     # PFEILTASTE
                result = maze.step(dir_helper.index(e.key));
                if (result[1]): yammie();
                if (result[0]): steps += 1;
                if (result[2]): TEXT = f'  ZIEL nach {steps} Steps, Essen: {len(maze.gegessen)}/{len(maze.gegessen) + len(maze.model.food)}';
                else: update_std_text();
                if (result[0]): render();
            elif (e.key == pg.K_0):
                maze.stein = list(maze.model.entry);
                render();
            elif (e.key == pg.K_ESCAPE): input_new();
            elif (e.key == pg.K_r): init(maze.model.x, maze.model.y);
        else: continue;  

print(f'QUIT AFTER {render_count} RENDER CYCLES.')
pg.quit();
