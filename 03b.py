from __future__ import annotations
import re
import itertools
import numpy as np


def label(matrix, intersection):
    for i in range(intersection[0], intersection[1]):
        for j in range(intersection[2], intersection[3]):
            matrix[i][j] = True


class Square:

    def __init__(self, id, left, top, width, height):
        self.id = int(id)
        self.left = int(left)
        self.top = int(top)
        self.width = int(width)
        self.height = int(height)
        self.not_intersects = True

    def right(self):
        return self.left + self.width

    def bottom(self):
        return self.top + self.height

    def intersects(self, sq2: Square):
        sq1 = self
        sq1_right = sq1.left > sq2.right()
        sq2_right = sq2.left > sq1.right()
        sq1_up = sq1.bottom() < sq2.top
        sq2_up = sq2.bottom() < sq1.top

        return not(sq1_right or sq2_right or sq1_up or sq2_up)

    def intersection(self, sq2: Square):
        sq1 = self
        new_left = max(sq1.left, sq2.left)
        new_right = min(sq1.right(), sq2.right())
        new_top = max(sq1.top, sq2.top)
        new_bottom = min(sq1.bottom(), sq2.bottom())
        return new_left, new_right, new_top, new_bottom

    def __str__(self) -> str:
        return "#{} [{},{}] [{},{}]".format(self.id, self.left, self.top, self.width, self.height)

    def __repr__(self) -> str:
        return str(self)


matrix = np.zeros((1000, 1000), dtype=np.bool_)
lines = [x.strip() for x in open("inputs/input03.txt").readlines()]
regex = re.compile(r"#(\d*) @ (\d*),(\d*): (\d*)x(\d*)")
squares = [Square(*regex.match(line).groups()) for line in lines]
combinations = itertools.combinations(squares, 2)
for (square1, square2) in combinations:
    if square1.intersects(square2):
        intersection = square1.intersection(square2)
        label(matrix, intersection)
        square1.not_intersects = False
        square2.not_intersects = False
res = list(filter(lambda square: square.not_intersects, squares))
print(res[0].id)
