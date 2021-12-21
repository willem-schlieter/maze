import random
from typing import *

# gibt Anzahl der Türen an, abhängig von der Länge der Wand, zB: "lambda len : 1 if len < 3 else random.randrange(1, 3)"
DOOR_COUNT = lambda len : 1 if len < 3 else random.randrange(1, 3) if len < 5 else random.randrange(1, 4)
# DOOR_COUNT = lambda len : 1

# DIM_CRIT gibt an, nach welchem Kriterium die Dimension einer Wand festgelegt wird.
#   RAND = zufällig (50% / 50%)
#   PROP = zufällig, aber je größer x im Verhältnis zu y,
#       desto wahrscheinlicher ist eine vertikale Wand
#   STRICT = vertikal, wenn x > y, sonst horizontal. bei x == y wie RAND.
DIM_CRIT = "PROP"

class Maze:
    def __init__(self, x: int, y: int, fill: bool = False):
        self.x = x
        self.y = y
        self.hw = [[False for j in range(self.x)] for i in range(self.y - 1)]                       # Erstellung der Matrix für horizontale Wände
        self.vw = [[False for j in range(self.y)] for i in range(self.x - 1)]                       # vertikale Wände
        self.entry = (0, 0);
        self.exit = (x - 1, y - 1);
        self.food = [];
        if (fill):                                                                                  # optionales Füllen des Labyrinthes
            self.recreate()

    def __str__(self):
        return str((self.hw, self.vw))
    
    def recreate(self, empty: bool = False):
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
                DIM_CRIT == "PROP" and random.randrange(x + y - 2) < x - 1 or
                DIM_CRIT == "STRICT" and x > y or
                (DIM_CRIT == "RAND" or x == y) and random.randrange(2)
            ):                                                                                      # vertikale Wand
                door = []
                for i in range(DOOR_COUNT(y)): door.append(random.randrange(y) + pos[1])            # Türen hinzufügen
                wall = random.randrange(x - 1)
                for i in range(pos[1], pos[1] + y):                                                 # alle Einträge in der vertikalen Wand
                    if (i not in door):
                        self.vw[wall + pos[0]][i] = True                                            # auf True setzen
                self.div(pos, wall + 1, y)                                                          # Rekursion mit linkem Teilbereich
                self.div((pos[0] + wall + 1, pos[1]), x - wall - 1, y)                              # Rekursion mit rechtem Teilbereich
            
            else:                                                                                   # horizontale Wand
                door = []
                for i in range(DOOR_COUNT(x)): door.append(random.randrange(x) + pos[0])            # Türen hinzufügen
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

    def shortest_way(self, a: tuple, b: tuple) -> int:
        matrix = [[0 for i in range(self.x)] for i in range(self.y)]
        matrix[a[0]][a[1]] = 1
        i = 1
        while (not matrix[b[0]][b[1]]):
            for i_1 in range(self.x):
                for i_2 in range(self.y):
                    if (matrix[i_1][i_2] == i):
                        if (not self.is_wall((i_1, i_2), 0) and not matrix[i_1][i_2 - 1]): matrix[i_1][i_2 - 1] = i + 1
                        if (not self.is_wall((i_1, i_2), 1) and not matrix[i_1 + 1][i_2]): matrix[i_1 + 1][i_2] = i + 1
                        if (not self.is_wall((i_1, i_2), 2) and not matrix[i_1][i_2 + 1]): matrix[i_1][i_2 + 1] = i + 1
                        if (not self.is_wall((i_1, i_2), 3) and not matrix[i_1 - 1][i_2]): matrix[i_1 - 1][i_2] = i + 1
            i += 1
        return matrix[b[0]][b[1]] - 1

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

    def walls(self, x, y):
        if (x not in range(self.x) or y not in range(self.y)):
            raise IndexError('The given field does not exist in the maze.')
        else:
            return (
                self.hw[y - 1][x] if y else True,
                self.vw[x][y] if x + 1 < self.x else True,
                self.hw[y][x] if y + 1 < self.y else True,
                self.vw[x - 1][y] if x else True
            )

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

    def rnd_field(self):
        return (random.randrange(self.x), random.randrange(self.y));

    def mkfood(self, count: int):
        if (count + 2 > (self.x * self.y)): raise ValueError("Too much food!");
        while len(self.food) < count:
            f = self.rnd_field();
            if (f != self.entry and f != self.exit and f not in self.food): self.food.append(f);

