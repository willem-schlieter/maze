import pygame as pg;
from maze import Maze;

DIM = (30, 30);
FELDBREITE = 30;
WANDBREITE = 10;
WANDFARBE = "#000000";
FENSTER = ((FELDBREITE + WANDBREITE) * DIM[0] + WANDBREITE, (FELDBREITE + WANDBREITE) * DIM[1] + WANDBREITE);

screen = pg.display.set_mode(FENSTER);
uhr = pg.time.Clock();
weiter = True;

maze = Maze(DIM[0], DIM[1], True);

def wand (x, y, h):
    pg.draw.rect(screen, WANDFARBE, (x, y, FELDBREITE if h else WANDBREITE, WANDBREITE if h else FELDBREITE));

def render ():
    screen.fill((0x4C, 0xAF, 0x50));
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

    pg.display.flip();

pg.init()
print(repr(maze));
render()

while weiter:
    uhr.tick(9)
    for e in pg.event.get():
        if (e.type == pg.QUIT): weiter = False;

pg.quit()