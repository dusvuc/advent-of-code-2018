import numpy as np
import re

class TimePoint:

    def __init__(self, year, month, day, hour, minute, guard_id=-1):
        self.guard_id = int(guard_id)
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int(hour)
        self.minute = int(minute)
        self.intervals = []

    def is_guard(self):
        return self.guard_id != -1

    def add_interval(self, interval: int):
        self.intervals.append(interval)

    def __repr__(self):
        if self.is_guard():
            str = "#{}: {}-{}-{} {}:{}".format(self.guard_id, self.year, self.month, self.day, self.hour, self.minute)
        else:
            str =  "{}-{}-{} {}:{}".format(self.year, self.month, self.day, self.hour, self.minute)
        if len(self.intervals):
            str += "\n{}".format(self.intervals)
        return str


class Day:
    def __init__(self, guard: str, intervals: list):
        awake = True
        self.id = guard
        self.days = np.zeros(60, dtype=np.bool_)
        for i in range(0, 60):
            if i in intervals:
                awake = not awake
            self.days[i] = awake

    def __repr__(self):
        return "#{}: {}".format(self.id, self.days)



guard_regex = re.compile("\[(\d*)\-(\d*)\-(\d*) (\d*):(\d*)\] Guard #(\d*) begins shift")
day_regex = re.compile("\[(\d*)\-(\d*)\-(\d*) (\d*):(\d*)\]*")
lines = [x.strip() for x in open("inputs/input04.txt").readlines()]
lines.sort()
timepoints = []

for line in lines:
    p = guard_regex.match(line)
    if p:
        timepoints.append(TimePoint(*p.groups()))
    else:
        p = day_regex.match(line)
        timepoints.append(TimePoint(*p.groups()))

for tp in timepoints:
    if tp.is_guard():
        current_guard = tp
    else:
        current_guard.add_interval(tp.minute)

for tp in timepoints:
    if tp.is_guard():
        print(tp)