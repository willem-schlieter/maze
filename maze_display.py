from typing import *
import pygame as pg
from maze import Maze as Model
import style


class Maze:
    def __init__ (self, model: Model):
        self.model = model
        self.x = model.x
        self.y = model.y
        self.stein = list(self.model.entry)
        self.render_count = 0
        self.gegessen = []
        self.init_size()
    # Aufrufen, wenn sich die (gewünschte) Größe des Maze-Surface verändert
    def init_size (self):
        self.grössen = (
            int((style.S_FELD + style.S_WAND()) * self.x + style.S_WAND()),
            int((style.S_FELD + style.S_WAND()) * self.y + style.S_WAND())
        )
        self.surface = pg.Surface(self.grössen)


    def wand (self, x: int, y: int, h: bool, screen) -> None:
        pg.draw.rect(self.surface, style.F_WAND, (x, y, style.S_FELD if h else style.S_WAND(), style.S_WAND() if h else style.S_FELD))
    
    def feld2pos (self, feld: Tuple[int, int]) -> Tuple[int, int]:
        return (style.S_WAND() + feld[0] * (style.S_WAND() + style.S_FELD), style.S_WAND() + feld[1] * (style.S_WAND() + style.S_FELD))

    def render (self) -> pg.Surface:
        self.render_count += 1
        # print("RENDER " + str(self.render_count))
        self.surface.fill(style.F_HG_END if tuple(self.stein) == self.model.exit else style.F_HG_STD)

        # RÄNDER
        # oben
        pg.draw.rect(self.surface, style.F_WAND, (0, 0, self.grössen[0], style.S_WAND()))
        # links
        pg.draw.rect(self.surface, style.F_WAND, (0, 0, style.S_WAND(), self.grössen[1]))
        # unten
        pg.draw.rect(self.surface, style.F_WAND, (0, self.grössen[1] - style.S_WAND(), self.grössen[0], style.S_WAND()))
        # rechts
        pg.draw.rect(self.surface, style.F_WAND, (self.grössen[0] - style.S_WAND(), 0, style.S_WAND(), self.grössen[1]))

        for y in range(self.y):
            for x in range(self.x):
                # Vertikale Wände
                if (x < (self.x - 1) and self.model.vw[x][y]):
                    self.wand(
                        style.S_WAND() + style.S_FELD + x * (style.S_FELD + style.S_WAND()),
                        style.S_WAND() + y * (style.S_FELD + style.S_WAND()),
                    False, self.surface)
                # Horizontale Wände
                if (y < (self.y - 1) and self.model.hw[y][x]):
                    self.wand(
                        style.S_WAND() + x * (style.S_FELD + style.S_WAND()),
                        style.S_WAND() + style.S_FELD + y * (style.S_FELD + style.S_WAND()),
                    True, self.surface)
        # Kreuzungen
        for y in range(1, self.y):
            for x in range(1, self.x):
                pg.draw.rect(self.surface, style.F_WAND, (x * (style.S_FELD + style.S_WAND()), (y * (style.S_FELD + style.S_WAND())), style.S_WAND(), style.S_WAND()))

        # FOOD
        for f in self.model.food: pg.draw.rect(self.surface, style.F_FOOD, (*self.feld2pos(f), style.S_FELD, style.S_FELD))

        if (self.stein != self.model.exit):
            # Spielstein
            pg.draw.rect(self.surface, style.F_ST, (*self.feld2pos(self.stein), style.S_FELD, style.S_FELD))
            # Ausgang
            pg.draw.rect(self.surface, style.F_EX, (*self.feld2pos(self.model.exit), style.S_FELD, style.S_FELD))

        return self.surface

    def step (self, dir: int) -> List[bool]:
        result = [False, False, False] # [gegangen, gegessen, exit]
        if not self.model.is_wall(self.stein, dir):
            self.stein[(dir + 1) % 2] += 1 if dir % 3 else -1
            result[0] = True
            if (tuple(self.stein) in self.model.food):
                self.gegessen.append(self.model.food.pop(self.model.food.index(tuple(self.stein))))
                result[1] = True
            if (tuple(self.stein) == self.model.exit):
                result[2] = True
        return result
