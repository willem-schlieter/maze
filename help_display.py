from typing import *
import pygame as pg;
import style;

cuts = [
    ("Pfeiltasten", "Navigation"),
    ("Escape", "Größe eingeben für neues Maze"),
    "ENDE"
]
FONT = pg.font.SysFont(*style.FONT)

def render (size):
    left = [];
    right = [];
    for c in cuts:
        if type(c) is tuple:
            left.append(FONT.render(f'  {c[0]}  ', False, style.F_HELP_HG, style.F_HELP_FG));
            right.append(FONT.render(f' – {c[1]}', True, style.F_HELP_FG, style.F_HELP_HG));
        else:
            left.append(FONT.render(c, True, style.F_HELP_FG, style.F_HELP_HG));
            ph = pg.Surface((1, left[len(left) - 1].get_height()))
            ph.fill(style.F_HELP_HG)
            right.append()

    lw = max(*[s.get_width() for s in left]);
    rw = max(*[s.get_width() for s in right]);
    item_height = lw[0].get_height();

    ls = pg.Surface((lw, len(left) * (item_height + style.HELP_Y_BUFFER)))
    rs = pg.Surface((rw, ls.get_height()))
    ypos = 0;
    for i in range(len(lw)):
        ls.blit(ls[i], (0, ypos))
        rs.blit(rs[i], (0, ypos))
        ypos += item_height + style.HELP_Y_BUFFER
    
    root = pg.Surface((lw + rw, ls.get_height()))
    root.fill(style.F_HELP_HG)
    

    return root;

