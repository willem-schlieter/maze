# Performance-Test

from maze import Maze;
from time import time;

for i in range (10, 1000, 100):
    t0 = time();
    m = Maze(i, i)
    t1 = time();
    m.recreate();
    t2 = time();

    print("Maze (size: {}) initialized in: {}".format(i, t1 - t0));
    print("Maze (size: {}) recreated in: {}".format(i, t2 - t1));
