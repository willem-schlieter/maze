from typing import *
import pygame as pg;
from maze import Maze;
import style;

render_count = 0;

def feld2pos (feld: Tuple[int, int]) -> Tuple[int, int]:
    return (style.S_WAND + feld[0] * (style.S_WAND + style.S_FELD), style.S_WAND + feld[1] * (style.S_WAND + style.S_FELD));

def wand (x: int, y: int, h: bool, screen):
    pg.draw.rect(screen, style.F_WAND, (x, y, style.S_FELD if h else style.S_WAND, style.S_WAND if h else style.S_FELD));

def pre_render (screen: pg.Surface, maze: Maze, STEIN: Tuple[int, int]):
    DIM = (maze.x, maze.y);
    FENSTER = ((style.S_FELD + style.S_WAND) * DIM[0] + style.S_WAND, (style.S_FELD + style.S_WAND) * DIM[1] + style.S_WAND);
    global render_count;
    render_count += 1;
    print("RENDER " + str(render_count))
    screen.fill(style.F_HG_END if tuple(STEIN) == maze.exit else style.F_HG_STD);

    # RÄNDER
    # oben
    pg.draw.rect(screen, style.F_WAND, (0, 0, FENSTER[0], style.S_WAND));
    # links
    pg.draw.rect(screen, style.F_WAND, (0, 0, style.S_WAND, FENSTER[1]));
    # unten
    pg.draw.rect(screen, style.F_WAND, (0, FENSTER[1] - style.S_WAND, FENSTER[0], style.S_WAND));
    # rechts
    pg.draw.rect(screen, style.F_WAND, (FENSTER[0] - style.S_WAND, 0, style.S_WAND, FENSTER[1]));

    for y in range(DIM[1]):
        for x in range(DIM[0]):
            # Vertikale Wände
            if (x < (DIM[0] - 1) and maze.vw[x][y]):
                wand(
                    style.S_WAND + style.S_FELD + x * (style.S_FELD + style.S_WAND),
                    style.S_WAND + y * (style.S_FELD + style.S_WAND),
                False, screen);
            # Horizontale Wände
            if (y < (DIM[1] - 1) and maze.hw[y][x]):
                wand(
                    style.S_WAND + x * (style.S_FELD + style.S_WAND),
                    style.S_WAND + style.S_FELD + y * (style.S_FELD + style.S_WAND),
                True, screen);
    for y in range(DIM[1] + 1):
        for x in range(DIM[0] + 1):
            pg.draw.rect(screen, style.F_WAND, (x * (style.S_FELD + style.S_WAND), (y * (style.S_FELD + style.S_WAND)), style.S_WAND, style.S_WAND));

    # FOOD
    for f in maze.food: pg.draw.rect(screen, style.F_FOOD, (*feld2pos(f), style.S_FELD, style.S_FELD));

    if (STEIN != maze.exit):
        # Spielstein
        pg.draw.rect(screen, style.F_ST, (*feld2pos(STEIN), style.S_FELD, style.S_FELD));
        # Ausgang
        pg.draw.rect(screen, style.F_EX, (*feld2pos(maze.exit), style.S_FELD, style.S_FELD));

    return render_count;
