class DoubleList:
    class Node:
        def __init__(self, value):
            self.next = None
            self.prev = None
            self.value = value

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_front(self, value):
        if not self.head:
            self.head = self.tail = self.Node(value)
        else:
            node = self.Node(value)
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def add_back(self, value):
        if not self.head:
            self.head = self.tail = self.Node(value)
        else:
            node = self.Node(value)
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    class ListIterator:
        def __init__(self, lst):
            self.current = lst.head

        def __next__(self):
            if not self.current:
                raise StopIteration
            else:
                val = self.current
                self.current = self.current.next
                return val

    def __iter__(self):
        return self.ListIterator(self)

    def __repr__(self):
        r1 = ""
        for node in self:
            if node.value.id % 10:
                r1 += " "
            else:
                r1 += str(node.value.id // 10)

        res = ""
        for node in self:
            res += str(node.value)
        return "{}\n{}".format(r1, res)


class Plant:
    id = 0

    def __init__(self, state, plant_id=0):
        if plant_id == 0:
            self.id = Plant.id
            Plant.id += 1
        else:
            self.id = plant_id
        self.plant = True if state == "#" else False
        self.next_plant = False

    def __eq__(self, other):
        return self.id.__eq__(other.id)

    def __lt__(self, other):
        return self.id.__lt__(other.id)

    def __repr__(self):
        return "#" if self.plant else "."


class Plants:

    def __init__(self, line, collections):
        self.first = 0
        self.last = 0
        self.combinations = dict()
        for comb in collections:
            follows = comb.split(" => ")
            inputs = tuple(sign == "#" for sign in follows[0])
            self.combinations[inputs] = (follows[1] == "#")

        self.plants = DoubleList()
        for i in range(-1, -3, -1):
            self.plants.add_back(Plant(".", i))
            self.first -= 1
        for data in line:
            self.last += 1
            self.plants.add_front(Plant(data))
        for i in range(0, 2):
            self.plants.add_front(Plant(".", self.last))
            self.last += 1


    def get_values(self, id: int):
        a, first, last = self.plants, self.first, self.last

        if first + 2 <= id <= last - 2:
            return a[id - 2].plant, a[id - 1].plant, a[id].plant, a[id + 1].plant, a[id + 2].plant
        if id == first:
            return False, False, a[id].plant, a[id + 1].plant, a[id + 2].plant
        if id == first + 1:
            return False, a[id - 1].plant, a[id].plant, a[id + 1].plant, a[id + 2].plant
        if id == last:
            return a[id - 2].plant, a[id - 1].plant, a[id].plant, False, False
        if id == last - 1:
            return a[id - 2].plant, a[id - 1].plant, a[id].plant, a[id + 1].plant, False

    def get_next_value(self, i):
        vals = self.get_values(i)
        return self.combinations[vals]

    def calculate(self):
        ps = self.plants
        for plant in ps:
            ll = plant.prev.prev.value.plant if plant.prev and plant.prev.prev else False
            l = plant.prev.value.plant if plant.prev else False
            rr = plant.next.next.value.plant if plant.next and plant.next.next else False
            r = plant.next.value.plant if plant.next else False
            c = plant.value.plant

            plant.value.next_plant = self.combinations[ll, l, c, r, rr]

        if ps.head.value.next_plant or ps.head.next.value.next_plant:
            ps.add_back(Plant(".", self.first))
            self.first -= 1
        if ps.tail.value.next_plant or ps.tail.prev.value.next_plant:
            ps.add_front(Plant(".", self.last))
            self.last += 1

    def add_to_left(self):
        self.first -= 1
        self.plants[self.first] = Plant(".", self.first)

    def add_to_right(self):
        self.last += 1
        self.plants[self.last] = Plant(".", self.last)

    def update(self):
        for plant in self.plants:
            plant.value.plant = plant.value.next_plant

    def __iter__(self):
        return self.plants.__iter__()

    def __repr__(self):
        return str(self.plants)


lines = [line.strip() for line in open("inputs/input12.txt") if line.strip()]
start, combs = lines[0], lines[1:]
start = start.strip("initial state: ")
plants = Plants(start, combs)
sum, last_sum = 0, 0
for i in range(0, 1000):
    sum = 0
    plants.calculate()
    plants.update()
    for pt in plants:
        if pt.value.plant:
            sum += pt.value.id
    last_sum = sum
    diff = sum - last_sum
sum = 22966 + 109 * (50000000000-200) #see diff stabilize (here, 109)
print(sum)