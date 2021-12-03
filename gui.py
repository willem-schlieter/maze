from typing import *
import pygame as pg
from maze import Maze as Model;
from maze_display import Maze;
import style;
pg.init();

DIM = (10, 10);
FOOD_COUNT = 1;

render_count = 0;
pfeiltasten = (pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT);
pg.display.set_icon(style.ICON);

STATE = "STD"; # STD | YAMMIE
TEXT = "";

def update_std_text () -> str:
    global TEXT;
    TEXT = f'  {maze.stein[0]}x{maze.stein[1]}    {len(maze.gegessen)}/{len(maze.gegessen) + len(maze.model.food)}    {steps} Steps    {style.S_FELD}*{style.F2W}';
    return TEXT;

def blit(parent: pg.Surface, child: pg.Surface, x: int = None, y: int = None) -> Tuple[int, int]:
    pos = (((parent.get_width() - child.get_width()) / 2) if x is None else x, ((parent.get_height() - child.get_height()) / 2) if y is None else y);
    parent.blit(child, pos);
    return pos;

def render (state: str = "", text: str = "") -> None:
    global render_count;
    render_count += 1;
    global TEXT, STATE;
    TEXT = text or TEXT; STATE = state or STATE;

    if (STATE == "STD"):
        MAIN.fill(style.F_HG);
        blit(MAIN, maze.render());
    elif (STATE == "YAMMIE"):
        MAIN.fill(style.F_FOOD);
        MAIN.blit(YAMMIE, ((FENSTER[0] - min(*FENSTER)) / 2, (FENSTER[1] - min(*FENSTER)) / 2));
        TEXT = "YAMMIE!";
    else: raise ValueError("Invalid render state: " + str(STATE));

    tsf = style.FONT.render(TEXT, True, "#eeeeee", "#444444");
    pg.draw.rect(SCREEN, "#444444", (0, FENSTER[1] - style.S_FOOT, FENSTER[0], style.S_FOOT));
    blit(SCREEN, tsf, y = FENSTER[1] - (style.S_FOOT * 0.9));

    SCREEN.blit(MAIN, (0, 0));
    pg.display.flip();

def new ():
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
                    cursor += 1;
                    weiter = cursor < 3;
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
        DIM = (int(newdim[0] or DIM[0]), int(newdim[1] or DIM[1]))
        FOOD_COUNT = int(newdim[2] or FOOD_COUNT)
        init();
    else: #Wurde abgbrochen
        update_std_text();
        render();

def init():
    global maze, FENSTER, SCREEN, uhr, steps, YAMMIE, MAIN;
    maze = Maze(Model(DIM[0], DIM[1], True));
    maze.model.mkfood(FOOD_COUNT % ((DIM[0] * DIM[1]) - 1));
    pg.display.set_caption(f'Maze {DIM[0]} x {DIM[1]}');
    uhr = pg.time.Clock();
    steps = 0;
    update_std_text();
    init_size(False);
    render();
def init_size (r: bool = True):
    global SCREEN, FENSTER, MAIN, YAMMIE;
    maze.init_size();
    FENSTER = (max(maze.grössen[0] + style.MIN_MARGIN, style.MIN_WIDTH), max(maze.grössen[1] + style.MIN_MARGIN, style.MIN_HEIGHT) + style.S_FOOT);
    SCREEN = pg.display.set_mode(FENSTER);
    MAIN = pg.Surface((FENSTER[0], FENSTER[1] - style.S_FOOT));
    YAMMIE = pg.transform.smoothscale(style.ICON, (min(*FENSTER), min(*FENSTER)));
    if r: render();
    # print(f'mazeSF: {maze.grössen[0]}, echt: {maze.surface.get_width()}   FENSTER: {FENSTER[0]}, echt: {SCREEN.get_width()}');
    # print(f'FELD: {style.S_FELD}  WAND: {style.S_WAND()}');

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
            print("KEYDOWN " + str(e.key))
            if (e.key in pfeiltasten):     # PFEILTASTE
                result = maze.step(pfeiltasten.index(e.key));
                if (result[1]):
                    render("YAMMIE");
                    pg.time.wait(400);
                    render("STD");
                if (result[0]): steps += 1;
                if (result[2]): TEXT = f'  ZIEL nach {steps} Steps, Essen: {len(maze.gegessen)}/{len(maze.gegessen) + len(maze.model.food)}';
                else: update_std_text();
                if (result[0]): render();
            elif (e.key == pg.K_0):
                maze.stein = list(maze.model.entry);
                render();
            elif (e.key == pg.K_ESCAPE): new();
            elif (e.key == pg.K_r): init();
            elif (e.key == pg.K_h): help(False); init();
            elif (e.key == pg.K_PLUS or e.key == pg.K_MINUS):
                dir = 1 if e.key == pg.K_PLUS else -1;
                if (style.S_FELD or dir == 1):
                    style.S_FELD += dir * style.S_FELD_MODIFY_STEP(max(maze.x, maze.y));
                    update_std_text();
                    init_size();
                    print(f"MODIFY FELD: {style.S_FELD} {style.F2W}")
            elif (e.key in (pg.K_COMMA, pg.K_PERIOD)):
                style.F2W = style.F2W_MODIFY(e.key == pg.K_PERIOD);
                update_std_text();
                init_size();
                print(f"MODIFY F2W. {style.S_FELD} {style.F2W}")

        else: continue;

print(f'QUIT AFTER {render_count} RENDER CYCLES.')
pg.quit();
