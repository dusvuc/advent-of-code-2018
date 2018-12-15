from __future__ import annotations

import itertools
import math
import string
from operator import *

ids = list(string.ascii_lowercase) + list("бгдђзиклњљптћуфхцчџшšćđč")


class Element:

    def __init__(self, x=0, y=0, line=""):
        if line != "":
            coordinates = [x.strip() for x in line.split(',')]
            x = int(coordinates[0])
            y = int(coordinates[1])
        self.x = x
        self.y = y
        self.minimal_distance = math.inf
        self.belongs_to = "#"

    def update(self, manhattan_distance: int, id: str):
        if self.minimal_distance > manhattan_distance:
            self.minimal_distance = manhattan_distance
            self.belongs_to = id
        elif self.minimal_distance == manhattan_distance:
            self.belongs_to = "#"

    def manhattan_distance(self, x: int, y: int) -> int:
        return abs(self.x - x) + abs(self.y - y)

    def is_point(self):
        return False

    def __repr__(self):
        return "({}, {}) min={}, belongs={}".format(self.x, self.y, self.minimal_distance,
                                                    self.belongs_to)


class Point(Element):
    id = 0

    def __init__(self, x=0, y=0, line=""):
        Element.__init__(self, x=x, y=y, line=line)
        self.id = ids[Point.id]
        Point.id += 1
        self.belongs_to = self.id.upper()

    def is_point(self):
        return True

    def __repr__(self):
        return "{}: ".format(self.id) + Element.__repr__(self)


def make_coords(filepath):
    lines = open(filepath, mode='r').readlines()
    coords = []
    for line in lines:
        if line != "":
            coordinates = [x.strip() for x in line.split(',')]
            x = int(coordinates[0])
            y = int(coordinates[1])
            coords.append((x, y))
    return coords


def print_string_from_grid(grid):
    my_string = ""
    for j in range(0, N):
        for i in range(0, N):
            my_string += grid[i][j].belongs_to + " "
        my_string += "\n"
    return my_string

def print_string_from_grid_distance(grid):
    my_string = ""
    for j in range(0, N):
        for i in range(0, N):
            my_string += str(grid[i][j].minimal_distance) + " "
        my_string += "\n"
    return my_string


def get_grid(coords, pointsmap):
    maxX = max(coords, key=itemgetter(0))[0] + 1
    maxY = max(coords, key=itemgetter(1))[1] + 1
    N = max(maxX, maxY)
    grid = [[] for _ in range(0, N)]
    for sublist in grid:
        sublist.extend([0 for _ in range(0, N)])
    for y in range(0, N):
        for x in range(0, N):
            if (x, y) in coords:
                grid[x][y] = pointsmap[(x, y)]
            else:
                grid[x][y] = Element(x=x, y=y)
    print(grid)
    return N, grid


pointsmap = {}
points = []
coords = make_coords("inputs/input06.txt")

for (x, y) in coords:
    pt = Point(x, y)
    points.append(pt)
    pointsmap[x, y] = pt

N, grid = get_grid(coords, pointsmap)
points = [grid[x][y] for (x, y) in coords if grid[x][y].is_point()]
print(points)

print_string_from_grid(grid)


minX = min(points, key=attrgetter('x')).x
minY = min(points, key=attrgetter('y')).x
maxX = max(points, key=attrgetter('x')).x
maxY = max(points, key=attrgetter('y')).y


for x in range(0, N):
    for y in range(0, N):
        location = grid[y][x]
        if not location.is_point():
            for point in points:
                distance = point.manhattan_distance(y, x)
                location.update(distance, point.id)


legit_points = [pt for pt in points if minX < pt.x < maxX and minY < pt.y < maxY]
points_counter = {code.id: 0 for code in legit_points}
unrolled_grid = list(itertools.chain.from_iterable(grid))
for el in unrolled_grid:
    if not el.is_point() and el.belongs_to in points_counter.keys():
        points_counter[el.belongs_to] += 1

print(max(points_counter.values()) + 1)