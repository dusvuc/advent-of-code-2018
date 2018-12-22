import re

from PIL import Image, ImageDraw


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Point:
    id = 0

    def __init__(self, position, velocity):
        self.id = Point.id
        Point.id += 1
        self.position = position
        self.velocity = velocity

    def tick(self):
        self.position = self.position + self.velocity

    def __repr__(self):
        return "Point #{}: position={}, velocity={}".format(self.id, self.position, self.velocity)


def get_points(filename):
    lines = [line.strip() for line in open(filename, mode="r").readlines()]
    regex = re.compile("position=<\s*(-?\d*),\s*(-?\d*)> velocity=<\s*(-?\d*),\s*(-?\d*)>")
    numbers = [regex.match(line).groups() for line in lines]
    numbers = [[int(val) for val in tpl] for tpl in numbers]
    points = [Point(Vector(val[0], val[1]), Vector(val[2], val[3])) for val in numbers]
    return points


def print_points(points, canvas, iteration):
    canvas_half = canvas / 2
    specific_pts = {(point.position.x, point.position.y) for point in points}
    legit_pts = {(pt[0] + canvas_half, pt[1] + canvas_half) for pt in specific_pts if
                 -canvas_half < pt[0] < canvas_half and -canvas_half < pt[1] < canvas_half}
    xs = [pts[0] for pts in specific_pts]
    min_x, max_x = min(xs), max(xs)
    ys = [pts[1] for pts in specific_pts]
    min_y, max_y = min(ys), max(ys)
    x_width = max_x - min_x
    y_width = max_y - min_y
    print(x_width, y_width)
    if len(legit_pts) == len(specific_pts):
        img = Image.new(mode="L", size=(canvas, canvas), color=255)
        # print(legit_pts)
        ImageDraw.Draw(img).point(list(legit_pts))
        img.save("outputs/10/img{}.png".format(iteration))

    """
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) in specific_pts:
                f.write("#")
            else:
                f.write(".")
        f.write("\n")
    f.close()
    """


points = get_points("inputs/input10.txt")
for i in range(0, 10000):
    for pt in points:
        pt.tick()
    print_points(points, 5000, i)
img = Image.new(mode="L", size=(300, 300), color=255)
vals = [(val, val) for val in range(0, 150)]
ImageDraw.Draw(img).point(vals)
img.save("test.png")
