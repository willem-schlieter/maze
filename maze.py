import random

class Maze:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hw = [[False for j in range(self.x)] for i in range(self.y - 1)]                       # Erstellung der Matrix für horizontale Wände
        self.vw = [[False for j in range(self.y)] for i in range(self.x - 1)]                       # vertikale Wände

    def __str__(self):
        return str((self.hw, self.vw))
    
    def recreate(self, empty: bool = False):
        self.hw = [[False for j in range(self.x)] for i in range(self.y - 1)]                       # Erstellung der Matrix für horizontale Wände
        self.vw = [[False for j in range(self.y)] for i in range(self.x - 1)]                       # vertikale Wände
        if (not empty):
            self.div((0, 0), self.x, self.y)

    def div(self, pos: tuple, x: int, y: int):
        if (pos[0] not in range(self.x) or pos[1] not in range(self.y)):
            raise IndexError('Position out of range of the maze.')
        if (x < 1 or y < 1):
            raise ValueError('X and Y are required to be positive ints.')
        if (pos[0] + x > self.x or pos[1] + y > self.y):
            raise IndexError('Given area is too big.')

        if (x == 1 or y == 1):
            pass
        else:
            if (random.randrange(x + y - 2) < x - 1):                                               # vertikale Wand
                door = random.randrange(y) + pos[1]
                wall = random.randrange(x - 1)
                for i in range(pos[1], pos[1] + y):                                                 # alle Einträge in der vertikalen Wand
                    if (i != door):
                        self.vw[wall + pos[0]][i] = True                                            # auf True setzen
                self.div(pos, wall + 1, y)                                                          # Rekursion mit linkem Teilbereich
                self.div((pos[0] + wall + 1, pos[1]), x - wall - 1, y)                              # Rekursion mit rechtem Teilbereich
            
            else:                                                                                   # horizontale Wand
                door = random.randrange(x) + pos[0]
                wall = random.randrange(y - 1)
                for i in range(pos[0], pos[0] + x):                                                 # alle Einträge in der horizontalen Wand
                    if (i != door):
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
        
    def shortest_way(self, a: tuple, b: tuple, n: tuple = None) -> int:
        if (a[0] not in range(self.x) or a[1] not in range(self.y)):
            raise IndexError('The given point A does not exist in the maze.')
        if (b[0] not in range(self.x) or b[1] not in range(self.y)):
            raise IndexError('The given point B does not exist in the maze.')

        if (a == b):                                                                                # Ziel erreicht
            return 0
        else:
            d = -1
            if (a[0] > 0 and (a[0] - 1, a[1]) != n and not self.vw[a[0] - 1][a[1]]):                # nach links
                e = self.shortest_way((a[0] - 1, a[1]), b, a) + 1
                if (e):
                    d = e
            if (a[0] < self.x - 1 and (a[0] + 1, a[1]) != n and not self.vw[a[0]][a[1]]):           # nach rechts
                e = self.shortest_way((a[0] + 1, a[1]), b, a) + 1
                if (e and (e < d or d == -1)):
                    d = e
            if (a[1] > 0 and (a[0], a[1] - 1) != n and not self.hw[a[1] - 1][a[0]]):                # nach oben
                e = self.shortest_way((a[0], a[1] - 1), b, a) + 1
                if (e and (e < d or d == -1)):
                    d = e
            if (a[1] < self.y - 1 and (a[0], a[1] + 1) != n and not self.hw[a[1]][a[0]]):           # nach unten
                e = self.shortest_way((a[0], a[1] + 1), b, a) + 1
                if (e and (e < d or d == -1)):
                    d = e
            return d

