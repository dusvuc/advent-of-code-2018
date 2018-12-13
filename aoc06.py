class Point:
    id = 0

    def __init__(self, line):
        vals = [x.strip() for x in line.split(',')]
        self.id = Point.id
        Point.id += 1
        self.x = vals[0]
        self.y = vals[1]

    def __repr__(self):
        return "Point #{}: [{}, {}]".format(self.id, self.x, self.y)


lines = open("inputs/input06.txt", mode='r').readlines()
points = [Point(line) for line in lines]
print(points)
