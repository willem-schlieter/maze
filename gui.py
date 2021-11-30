from typing import *
import pygame as pg;
from maze import Maze;

DIM = (5, 5);
FELDBREITE = 20;
WANDBREITE = 10;
HGFARBEN = ("#ec4545", "#4caf50");
WANDFARBE = "#000000";
STEINFARBE = "#4caf50";
EXITFARBE = "#ffffff";
FOODFARBE = "#ffff00";
FENSTER = ((FELDBREITE + WANDBREITE) * DIM[0] + WANDBREITE, (FELDBREITE + WANDBREITE) * DIM[1] + WANDBREITE);

YAMMIE = pg.transform.smoothscale(pg.image.load("yammie.png"), (min(*FENSTER), min(*FENSTER)))

class Stein_Position:
    x = 0;
    y = 5;
    def __getitem__ (self, key: int):
        if (key not in (0, 1)): raise TypeError("Key must be in (0, 1).");
        else: return self.y if key else self.x;
    def __iadd__ (self, other: Tuple[int, int]):
        if (type(other) != tuple): raise TypeError("Only Tuples can be added to STEIN.");
        else:
            self.x += other[0];
            self.y += other[1];

screen = pg.display.set_mode(FENSTER);
uhr = pg.time.Clock();
weiter = True;
gegessen = [];

maze = Maze(DIM[0], DIM[1], True);
STEIN = list(maze.entry);
maze.create_food(4);

render_count = 0;

def feld2pos (feld: Tuple[int, int]) -> Tuple[int, int]:
    return (WANDBREITE + feld[0] * (WANDBREITE + FELDBREITE), WANDBREITE + feld[1] * (WANDBREITE + FELDBREITE));

def wand (x: int, y: int, h: bool):
    pg.draw.rect(screen, WANDFARBE, (x, y, FELDBREITE if h else WANDBREITE, WANDBREITE if h else FELDBREITE));

def render ():
    global render_count;
    render_count += 1;
    print("RENDER " + str(render_count))
    screen.fill(HGFARBEN[int(tuple(STEIN) == maze.exit)]);

    # RÄNDER
    # oben
    pg.draw.rect(screen, WANDFARBE, (0, 0, FENSTER[0], WANDBREITE));
    # links
    pg.draw.rect(screen, WANDFARBE, (0, 0, WANDBREITE, FENSTER[1]));
    # unten
    pg.draw.rect(screen, WANDFARBE, (0, FENSTER[1] - WANDBREITE, FENSTER[0], WANDBREITE));
    # rechts
    pg.draw.rect(screen, WANDFARBE, (FENSTER[0] - WANDBREITE, 0, WANDBREITE, FENSTER[1]));

    for y in range(DIM[1]):
        for x in range(DIM[0]):
            # Vertikale Wände
            if (x < (DIM[0] - 1) and maze.vw[x][y]):
                wand(
                    WANDBREITE + FELDBREITE + x * (FELDBREITE + WANDBREITE),
                    WANDBREITE + y * (FELDBREITE + WANDBREITE),
                False);
            # Horizontale Wände
            if (y < (DIM[1] - 1) and maze.hw[y][x]):
                wand(
                    WANDBREITE + x * (FELDBREITE + WANDBREITE),
                    WANDBREITE + FELDBREITE + y * (FELDBREITE + WANDBREITE),
                True);
    for y in range(DIM[1] + 1):
        for x in range(DIM[0] + 1):
            pg.draw.rect(screen, WANDFARBE, (x * (FELDBREITE + WANDBREITE), (y * (FELDBREITE + WANDBREITE)), WANDBREITE, WANDBREITE));

    # FOOD
    for f in maze.food: pg.draw.rect(screen, FOODFARBE, (*feld2pos(f), FELDBREITE, FELDBREITE));

    if (STEIN != maze.exit):
        # Spielstein
        pg.draw.rect(screen, STEINFARBE, (*feld2pos(STEIN), FELDBREITE, FELDBREITE));
        # Ausgang
        pg.draw.rect(screen, EXITFARBE, (*feld2pos(maze.exit), FELDBREITE, FELDBREITE));

    pg.display.flip();

pg.init()
render()

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
                    render();
                    screen.blit(YAMMIE, ((FENSTER[0] - min(*FENSTER)) / 2, (FENSTER[1] - min(*FENSTER)) / 2))
                    pg.display.flip();
                    pg.time.wait(1000);

            elif (e.key == pg.K_0): STEIN = maze.entry;
            render();
        else: continue;
            

pg.quit()