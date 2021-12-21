import random
from typing import *

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
            a += "|  "
            for j in range(self.x - 1):                                                             # vertikale Wände in dieser Zeile
                a += "|" if self.vw[j][i] else " "
                a += "  "
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
        data = [boo for row in self.hw for boo in row] + [boo for row in self.vw for boo in row];
        intarray = [self.x, self.y] + [int("".join([str(c) for c in a]), 2) for a in [[int(data.pop(0)) for j in range(8) if data] for i in range(0, len(data), 8)]];
        print(intarray)
        f = open(path, "wb");
        f.write(bytes(intarray));
        f.close();

    def from_file(path):
        if (type(path) == Maze): raise TypeError("from_file is a static method.");
        f = open(path, "rb");
        intarray = list(f.read());
        print(intarray)
        f.close();

        maze = Maze(intarray.pop(0), intarray.pop(0), False);

        data = [item for sublist in [[bool(int(n)) for n in list(bin(i)[2:])] for i in intarray] for item in sublist];
        while (len(data) < ((maze.x - 1) * maze.y + (maze.y - 1) * maze.x)):
            data.insert(False, 0)
        print(data);

        maze.hw = [[bool(data.pop(0)) for i in range(maze.y) if data] for i in range(maze.x - 1)];
        maze.vw = [[bool(data.pop(0)) for i in range(maze.x) if data] for i in range(maze.y - 1)];
        return maze;

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

