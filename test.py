# Performance-Test

from maze import Maze;
from time import time;

t0 = time();

m = Maze(200, 100)

t1 = time();

m.recreate();

t2 = time();

print("Maze initialized in: " + t1 - t0);
print("Maze recreated in: " + t2 - t1);
