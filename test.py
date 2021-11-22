# Performance-Test

from maze import Maze;
from time import time;

for i in range (10, 1000, 100):
    t0 = time()
    m = Maze(i, i)
    t1 = time()
    m.recreate()
    t2 = time()

    print("Maze (size: {}) initialized in:\t{}s".format(i, t1 - t0))
    print("Maze (size: {}) recreated in:\t\t{}s".format(i, t2 - t1))

t_i = 0
t_r = 0
for i in range (100):
    t0 = time()
    m = Maze(100, 100)
    t1 = time()
    m.recreate()
    t2 = time()

    t_i = t_i + (t1 - t0)
    t_r = t_r + (t2 - t1)
print('Für die Erstellung von 100 Labyrinthen der Größe 100*100 wurde die Zeit gemessen:\n   Initialisierung:\trund {}s\n   Wanderstellung:\trund {}s\n   Gesamt:\t\trund {}s'.format(round(t_i, 5), round(t_r, 5), round(t_i + t_r, 5)))
