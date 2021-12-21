import random
from typing import *
import json

class Maze:
    def __init__(self, x: int, y: int, fill: bool = False):
        self.x = x
        self.y = y
        self.hw = [[False for j in range(self.x)] for i in range(self.y - 1)]                       # Erstellung der Matrix für horizontale Wände
        self.vw = [[False for j in range(self.y)] for i in range(self.x - 1)]                       # vertikale Wände
        self.entry = (0, 0)
        self.exit = (x - 1, y - 1)
        self.food = []

        # DIM_CRIT gibt an, nach welchem Kriterium die Dimension einer Wand festgelegt wird.
        #   RAND = zufällig (50% / 50%)
        #   PROP = zufällig, aber je größer x im Verhältnis zu y,
        #       desto wahrscheinlicher ist eine vertikale Wand
        #   STRICT = vertikal, wenn x > y, sonst horizontal. bei x == y wie RAND.
        self.dim_crit = "PROP"
        # Wieviel Prozent der Wand (mit Ausnahme der einen vorgegebenen Tür) sind Türen?
        # 0 = 1 Tür. >99 = Keine Wände
        self.door_perc = 50

        if (fill): self.recreate()                                                                  # optionales Füllen des Labyrinthes

    def __str__(self):
        return str((self.hw, self.vw))
    
    def recreate(self, empty: bool = False, dim_crit: str = "", door_perc: int = -1):
        self.dim_crit = dim_crit or self.dim_crit
        self.door_perc = door_perc if door_perc + 1 else self.door_perc
        self.hw = [[False for j in range(self.x)] for i in range(self.y - 1)]                       # Erstellung der Matrix für horizontale Wände
        self.vw = [[False for j in range(self.y)] for i in range(self.x - 1)]                       # vertikale Wände
        if (not empty):
            self.div((0, 0), self.x, self.y)
            self.exit = self.farest_field(self.entry)
        return self

    def div(self, pos: Tuple[int, int], x: int, y: int):
        if (pos[0] not in range(self.x) or pos[1] not in range(self.y)):
            raise IndexError('Position out of range of the maze.')
        if (x < 1 or y < 1):
            raise ValueError('X and Y are required to be positive ints.')
        if (pos[0] + x > self.x or pos[1] + y > self.y):
            raise IndexError('Given area is too big.')

        if (x == 1 or y == 1):                                                                      # Zelle zu klein
            pass
        else:
            if (
                self.dim_crit == "PROP" and random.randrange(x + y - 2) < x - 1 or
                self.dim_crit == "STRICT" and x > y or
                (self.dim_crit == "RAND" or x == y) and random.randrange(2)
            ):                                                                                      # vertikale Wand
                door = []
                for i in range(int(self.door_perc * (y - 1) / 100) + 1):
                    door.append(random.randrange(y) + pos[1])                                       # Türen hinzufügen
                wall = random.randrange(x - 1)
                for i in range(pos[1], pos[1] + y):                                                 # alle Einträge in der vertikalen Wand
                    if (i not in door):
                        self.vw[wall + pos[0]][i] = True                                            # auf True setzen
                self.div(pos, wall + 1, y)                                                          # Rekursion mit linkem Teilbereich
                self.div((pos[0] + wall + 1, pos[1]), x - wall - 1, y)                              # Rekursion mit rechtem Teilbereich
            
            else:                                                                                   # horizontale Wand
                door = []
                for i in range(int(self.door_perc * (x - 1) / 100) + 1):
                    door.append(random.randrange(x) + pos[0])                                       # Türen hinzufügen
                wall = random.randrange(y - 1)
                for i in range(pos[0], pos[0] + x):                                                 # alle Einträge in der horizontalen Wand
                    if (i not in door):
                        self.hw[wall + pos[1]][i] = True                                            # auf True setzen
                self.div(pos, x, wall + 1)                                                          # Rekursion mit oberem Teilbereich
                self.div((pos[0], pos[1] + wall + 1), x, y - wall - 1)                              # Rekursion mit unterem Teilbereich

    def __repr__(self):
        a = "+"
        for i in range(self.x):                                                                     # erste Zeile (durchgehend)
            a += "--+"
        a += "\n"
        for i in range(self.y):                                                                     # je zwei Zeilen
            a += "|" + ("<>" if (0, i) in self.food else "  ")
            for j in range(self.x - 1):                                                             # vertikale Wände in dieser Zeile
                a += "|" if self.vw[j][i] else " "
                a += ("<>" if (j + 1, i) in self.food else "  ")
            a += "|\n+"                                                                             # Zeilenende
            if (i < self.y - 1):                                                                    # nicht in der letzten Iteration, da weniger Zeilen als Spalten (Einträge)
                for j in range(self.x):                                                             # horizontale Wände in dieser Zeile
                    a += "--" if self.hw[i][j] else "  "
                    a += "+"
                a += "\n"
        for i in range(self.x):                                                                     # abschließende Zeile
            a += "--+"
        return a
        
    def __eq__(self, other):
        if (type(other) == type(self)):
            return self.hw == other.hw and self.vw == other.vw;
        else:
            return NotImplemented;

    def __add__(self, other):
        if (type(other) != type(self)):
            raise TypeError("Both operands must be Mazes.")
        elif (self.y != other.y):
            raise ValueError("Mazes must have the same 'y'.")
        else:
            m = Maze(self.x + other.x, self.y)
            m.door_perc = (self.door_perc + other.door_perc) / 2
            trennwand = [True for i in range(self.y)]
            for i in range(int(m.door_perc * (self.y - 1) / 100) + 1):
                trennwand[random.randrange(len(trennwand))] = False
            m.vw = [*self.vw, trennwand, *other.vw]
            m.hw = [self.hw[i] + other.hw[i] for i in range(self.y - 1)]
            m.entry = (0, 0)
            m.exit = m.farest_field(m.entry)
            m.food = [*self.food, *[(f[0] + self.x, f[1]) for f in other.food]]

        return m

    def shortest_way_BAK(self, a: tuple, b: tuple, n: tuple = None) -> int:
        if (a[0] not in range(self.x) or a[1] not in range(self.y)):
            raise IndexError('The given point A does not exist in the maze.')
        if (b[0] not in range(self.x) or b[1] not in range(self.y)):
            raise IndexError('The given point B does not exist in the maze.')

        if (a == b):                                                                                # Ziel erreicht
            return 0
        else:                                                                                       # es gibt nur einen Weg, deshalb ist bei einem Weg dieser sofort richtig
            d = 0
            if (a[0] > 0 and (a[0] - 1, a[1]) != n and not self.vw[a[0] - 1][a[1]]):                # nach links
                d = self.shortest_way((a[0] - 1, a[1]), b, a) + 1
                if (d > 0):
                    return d
            if (a[0] < self.x - 1 and (a[0] + 1, a[1]) != n and not self.vw[a[0]][a[1]]):           # nach rechts
                d = self.shortest_way((a[0] + 1, a[1]), b, a) + 1
                if (d > 0):
                    return d
            if (a[1] > 0 and (a[0], a[1] - 1) != n and not self.hw[a[1] - 1][a[0]]):                # nach oben
                d = self.shortest_way((a[0], a[1] - 1), b, a) + 1
                if (d > 0):
                    return d
            if (a[1] < self.y - 1 and (a[0], a[1] + 1) != n and not self.hw[a[1]][a[0]]):           # nach unten
                d = self.shortest_way((a[0], a[1] + 1), b, a) + 1
                if (d > 0):
                    return d
            return -1

    def path_matrix(self, a: tuple) -> int:
        matrix = {}
        for x in range(self.x):
            for y in range(self.y): matrix[(x, y)] = 0

        matrix[a] = 1
        i = 1
        weiter = True
        while (weiter):
            weiter = False
            for i_1 in range(self.x):
                for i_2 in range(self.y):
                    if (matrix[(i_1, i_2)] == i):
                        if (not self.is_wall((i_1, i_2), 0) and not matrix[(i_1, i_2 - 1)]): matrix[(i_1, i_2 - 1)] = i + 1
                        if (not self.is_wall((i_1, i_2), 1) and not matrix[(i_1 + 1, i_2)]): matrix[(i_1 + 1, i_2)] = i + 1
                        if (not self.is_wall((i_1, i_2), 2) and not matrix[(i_1, i_2 + 1)]): matrix[(i_1, i_2 + 1)] = i + 1
                        if (not self.is_wall((i_1, i_2), 3) and not matrix[(i_1 - 1, i_2)]): matrix[(i_1 - 1, i_2)] = i + 1
                        weiter = True
            i += 1
        return matrix

    def shortest_path(self, a: tuple, b: tuple) -> int:
        return self.path_matrix(a)[b] - 1

    def farest_field(self, a: Tuple[int, int]) -> Tuple[int, int]:
        m = self.path_matrix(a)
        long = max(m.values())
        farest = [f for f in m.keys() if m[f] == long]
        return farest[random.randrange(len(farest))]

    def save(self, path: str):
        dic = {
            "size": (self.x, self.y),
            "dim_crit": self.dim_crit,
            "door_perc": self.door_perc,
            "entry": self.entry,
            "exit": self.exit,
            "hw": self.hw,
            "vw": self.vw,
            "food": self.food            
        }
        f = open(path, "w")
        f.write(json.dumps(dic))
        f.close()

    def load(self, path):
        f = open(path, "r")
        dic = json.loads(f.read())
        f.close()
        (self.x, self.y) = dic["size"]
        self.dim_crit = dic["dim_crit"]
        self.door_perc = dic["door_perc"]
        self.entry = dic["entry"]
        self.exit = dic["exit"]
        self.hw = dic["hw"]
        self.vw = dic["vw"]
        self.food = dic["food"]
        return self

    # Nimmt die Position eines Feldes und einen int "dir" entgegen und gibt an, ob in der angegebenen Richtung von dem Feld aus eine Wand ist. dir: (oben=0, links=1, unten=2, rechts=3)
    def is_wall(self, pos: Tuple[int, int], dir: int) -> bool:
        if (pos[0] not in range(self.x) or pos[1] not in range(self.y)):
            raise IndexError('The given field does not exist in the maze.')
        elif (dir not in range(4)):
            raise IndexError('"dir" out of range.')
        else:
            return not (
                (dir == 0 and pos[1] != 0 and not self.hw[pos[1] - 1][pos[0]]) or
                (dir == 1 and pos[0] != self.x - 1 and not self.vw[pos[0]][pos[1]]) or
                (dir == 2 and pos[1] != self.y - 1 and not self.hw[pos[1]][pos[0]]) or
                (dir == 3 and pos[0] != 0 and not self.vw[pos[0] - 1][pos[1]]))

    def rnd_field(self) -> Tuple[int, int]:
        return (random.randrange(self.x), random.randrange(self.y));

    def mkfood(self, count: int):
        if (count + 2 > (self.x * self.y)): raise ValueError("Too much food!")
        while len(self.food) < count:
            f = self.rnd_field()
            if (f != self.entry and f != self.exit and f not in self.food): self.food.append(f)
        return self

