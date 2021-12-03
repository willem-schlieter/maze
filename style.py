import pygame as pg;
pg.init();

F_HG_STD = "#ec4545"
F_HG_END = "#4caf50"
F_HG = "#333333";
F_WAND = "#000000"
F_ST = "#4caf50"
F_EX = "#ffffff"
F_FOOD = "#ffd918" # Hintergrundfarbe vom "Yammie"-Bild

S_FELD = 20
# nimmt die Feldanzahl der längeren Maze-Seite entgegen
# und gibt zurück, wie viel S_FELD pro +/- verändert
# werden soll.
S_FELD_MODIFY_STEP = lambda a : int(a * (S_FELD + S_FELD * F2W) / (10 * a)) or 1;
F2W_MODIFY = lambda dir : (F2W * 10 + (1 if dir else -1)) / 10 or F2W;
F2W = 0.1; # NUR EINE NACHKOMMASTELLE!
S_WAND = lambda : int(S_FELD * F2W);
S_FOOT = 30

MIN_WIDTH = 400;
# Exklusive Footer!
MIN_HEIGHT = 400;
MIN_MARGIN = 20;

FONT = pg.font.SysFont("times", int(S_FOOT * 0.75));
ICON = pg.image.load("yammie.png");
