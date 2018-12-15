import re
import itertools


def get_dependencies(filename):
    line_template = 'Step (\S) must be finished before step (\S) can begin.'
    regex = re.compile(line_template)
    lines = [line.strip() for line in open(filename, "r").readlines()]
    dependencies = [regex.match(line).groups() for line in lines]
    return dependencies


def get_next_visitable(unvisited):
    unvisitable = [node for node in unvisited if node.can_be_visited(unvisited)]
    return list(sorted(unvisitable))[0]


class GraphNode:
    def __init__(self, node_name):
        self.links = []
        self.depends_on = []
        self.name = node_name
        self.is_visited = False

    def add(self, node):
        self.links.append(node)
        node.depends_on.append(self)
        self.links.sort()

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def is_dependent(self):
        return len(self.depends_on)

    def can_be_visited(self, unvisited):
        for x in self.depends_on:
            if x in unvisited:
                return False
        return True

    def visit(self, unvisited):
        text = self.name
        self.is_visited = True
        unvisited.remove(self)
        while len(unvisited):
            to_visit = get_next_visitable(unvisited)
            to_visit.is_visited = True
            text += to_visit.name
            unvisited.remove(to_visit)
        return text


dependencies = get_dependencies("inputs/input07.txt")
values = set(itertools.chain.from_iterable(dependencies))
values = {name: GraphNode(name) for name in values}
for (X, Y) in dependencies:
    values[X].add(values[Y])  # X points to Y & Y is labeled as pointed to
unpointed = sorted(list(x for x in values.values() if not x.is_dependent()))
unvisited = list(values.values())
print(unpointed[0].visit(unvisited))
