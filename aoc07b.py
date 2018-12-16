import re
import itertools
from aoc07a import *


class Job:
    min_time = 60

    def __init__(self, graph_node: GraphNode):
        self.graph_node = graph_node
        self.duration = Job.min_time + Job.get_duration(graph_node.name)

    def __repr__(self):
        return "[{}], {} s remaining".format(self.graph_node.name, self.duration)

    @staticmethod
    def get_duration(letter: str) -> int:
        return ord(letter) - 64  # A = 1, B = 2...

    def is_over(self):
        return self.duration <= 0

    def tick(self):
        self.duration = self.duration - 1


class Worker:
    id = 1

    def __init__(self):
        self.id = Worker.id
        Worker.id += 1
        self.job = None

    def has_job(self):
        return self.job is not None

    def tick(self):
        if self.job:
            self.job.tick()

    def is_over(self):
        if self.job:
            return self.job.is_over()
        return True

    def finish_job(self):
        node = self.job.graph_node
        self.job = None
        return node

    def take_job(self, graph_node: GraphNode):
        self.job = Job(graph_node)

    def __repr__(self):
        res = "Worker #{}".format(self.id)
        if self.has_job():
            res += "job{}".format(self.job)
        return res


def get_all_visitables(unvisited, queued):
    visitables = [node for node in unvisited if node.can_be_visited(unvisited)]
    visitables = [visitable for visitable in visitables if visitable not in queued]
    return list(sorted(visitables))


def visit_schedule(unvisited, number_of_workers):
    workers = [Worker() for _ in range(0, number_of_workers)]
    minute = 0
    output = ""
    queued = []
    while len(unvisited) or any(map(lambda w: not w.is_over(), workers)):

        #  check if workers have finished, and append their work to the output
        done_workers = [worker for worker in workers if worker.has_job() and worker.is_over()]
        result = [worker.finish_job() for worker in done_workers]
        for graph_node in result:
            unvisited.remove(graph_node)
        result = [graph_node.name for graph_node in result]
        result.sort()
        result = "".join(result)
        output += result

        #  get free workers and available jobs, and then append jobs to workers
        free_workers = [worker for worker in workers if not worker.has_job()]
        can_visit = get_all_visitables(unvisited, queued)
        while len(free_workers) and len(can_visit):
            worker = free_workers.pop(0)
            visitable = can_visit.pop(0)
            queued.append(visitable)
            worker.take_job(visitable)

        # tick existing workers
        for worker in workers:
            worker.tick()
        minute += 1
    return minute - 1


dependencies = get_dependencies("inputs/input07.txt")
values = set(itertools.chain.from_iterable(dependencies))
values = {name: GraphNode(name) for name in values}
for (X, Y) in dependencies:
    values[X].add(values[Y])  # X points to Y & Y is labeled as pointed to
unvisited = list(values.values())
print(visit_schedule(unvisited, 5))
