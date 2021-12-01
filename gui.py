from typing import *
import pygame as pg
from pygame import surface;
from maze import Maze as Model;
from maze_display import Maze;
import style;
pg.init();

DIM = (10, 10);
FOOD_COUNT = 1;

FONT = pg.font.SysFont("times", int(style.S_FOOT * 0.75));
render_count = 0;
dir_helper = (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT);
ICON = pg.image.load("yammie.png");
pg.display.set_icon(ICON);

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
    text = FONT.render(TEXT, True, "#eeeeee", "#444444");
    pg.draw.rect(SCREEN, "#444444", (0, FENSTER[1] - style.S_FOOT, FENSTER[0], style.S_FOOT));
    SCREEN.blit(text, (0, FENSTER[1] - (style.S_FOOT * 0.9)))

    pg.display.flip();

def input_new ():
    def subrender():
        global TEXT;
        TEXT = f' Neu: {newdim[0]}{"_" if not cursor else ""} x {newdim[1] + ("_" if cursor == 1 else "")}  Essen: {newdim[2]}{"_" if cursor == 2 else ""}';
        render();
    newdim = ["", "", ""];
    cursor = 0;
    subrender();
    weiter = True;
    while weiter:
        uhr.tick(40);
        for e in pg.event.get():
            if (e.type == pg.KEYDOWN):
                if (e.key == pg.K_ESCAPE): weiter = False;
                elif (e.key == pg.K_RETURN):
                    if (newdim[cursor]):
                        cursor += 1;
                        weiter = cursor < 3;
                        subrender();
                    else:
                        TEXT = "EINGABE BITTE!"; render();
                        pg.time.wait(1000);
                        subrender();
                elif (e.key in range(48, 58)):
                    newdim[cursor] += str(e.key - 48);
                    subrender();
                elif (e.key == pg.K_BACKSPACE):
                    if (newdim[cursor]): newdim[cursor] = newdim[cursor][:-1];
                    else: cursor -= 1;
                    if (cursor == -1): weiter = False;
                    else: subrender();
                elif (e.key == pg.K_LEFT and cursor):
                    cursor -= 1;
                    subrender();
                elif (e.key == pg.K_RIGHT and cursor < 2):
                    cursor += 1;
                    subrender();

    if (cursor == 3):
        global DIM, FOOD_COUNT;
        DIM = (int(newdim[0]), int(newdim[1]))
        FOOD_COUNT = int(newdim[2])
        init();
    else: #Wurde abgbrochen
        update_std_text();
        render();

def init():
    global maze, FENSTER, SCREEN, uhr, steps, YAMMIE;
    maze = Maze(Model(DIM[0], DIM[1], True));
    maze.model.mkfood(FOOD_COUNT % ((DIM[0] * DIM[1]) - 1));
    FENSTER = (maze.grössen[0], maze.grössen[1] + style.S_FOOT);
    SCREEN = pg.display.set_mode(FENSTER);
    pg.display.set_caption(f'Maze {DIM[0]} x {DIM[1]}');
    uhr = pg.time.Clock();
    steps = 0;
    YAMMIE = pg.transform.smoothscale(ICON, (min(*FENSTER), min(*FENSTER)));
    update_std_text();
    render();

def help(start):
    SCREEN = pg.display.set_mode((400, 400));
    if (start): pg.display.set_caption("Willkommen bei MAZE!");
    uhr = pg.time.Clock();
    SCREEN.blit(pg.transform.smoothscale(pg.image.load("start.png" if start else "help.png"), (400, 400)), (0, 0));
    pg.display.flip();
    weiter = True;
    while weiter:
        uhr.tick(40);
        for e in pg.event.get(): weiter = not (e.type == pg.KEYDOWN and e.key == pg.K_RETURN);

help(True);
init();

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
            elif (e.key == pg.K_r): init();
            elif (e.key == pg.K_h): help(False); init();
        else: continue;  

print(f'QUIT AFTER {render_count} RENDER CYCLES.')
pg.quit();
