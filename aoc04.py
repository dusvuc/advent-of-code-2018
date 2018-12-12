import numpy as np
import re
import operator
from typing import *


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
            text = "#{}: {}-{}-{} {}:{}".format(self.guard_id, self.year, self.month, self.day, self.hour, self.minute)
        else:
            text = "{}-{}-{} {}:{}".format(self.year, self.month, self.day, self.hour, self.minute)
        if len(self.intervals):
            text += "\n{}".format(self.intervals)
        return text


class Day:
    def __init__(self, timepoint: TimePoint):
        self.day = timepoint.day
        self.month = timepoint.month
        self.year = timepoint.year
        self.guard_id = timepoint.guard_id

        self.minutes = np.zeros(60, dtype=np.bool_)
        awake = True
        for i in range(0, 60):
            if i in timepoint.intervals:
                awake = not awake
            self.minutes[i] = awake

    def __repr__(self):
        return "#{}: {}".format(self.id, self.minutes)


def create_timepoints(input_file):
    guard_regex = re.compile("\[(\d*)\-(\d*)\-(\d*) (\d*):(\d*)\] Guard #(\d*) begins shift")
    day_regex = re.compile("\[(\d*)\-(\d*)\-(\d*) (\d*):(\d*)\]*")
    lines = [x.strip() for x in open(input_file).readlines()]
    lines.sort()
    timepoints = []

    for line in lines:
        p = guard_regex.match(line)
        if p:
            timepoints.append(TimePoint(*p.groups()))
        else:
            p = day_regex.match(line)
            timepoints.append(TimePoint(*p.groups()))
    return timepoints


def to_intervals(timepoints):
    for tp in timepoints:
        if tp.is_guard():
            current_guard = tp
        else:
            current_guard.add_interval(tp.minute)
    return list(filter(lambda tp: tp.is_guard(), timepoints))


def find_sleepiest_guard(days: list):
    val = {}
    for day in days:
        if day.guard_id not in val:
            val[day.guard_id] = 0
        val[day.guard_id] += (day.minutes == False).sum()
    sorted_vals = sorted(val.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_vals[0][0]  # highest sorted, get item 0 (id)


def find_most_common_minute(days: List[Day], guard_id: int):
    minute_counts = np.zeros(60, dtype=np.int64)
    days = [day for day in days if day.guard_id == guard_id]
    for day in days:
        for i in range(0, 60):
            if not day.minutes[i]:
                minute_counts[i] += 1
    return minute_counts.argmax()


def find_highest_resting_guard_for_any_minute(days):
    all_guards = {}
    for day in days:
        if day.guard_id not in all_guards:
            guard_minutes = all_guards[day.guard_id] = np.zeros(60, dtype=np.int64)
        else:
            guard_minutes = all_guards[day.guard_id]
        for minute_id in range(0, 60):
            if not day.minutes[minute_id]:
                guard_minutes[minute_id] += 1
    all_guards = [(guard_id, minute_list.argmax(), minute_list.max()) for (guard_id, minute_list) in all_guards.items()]
    all_guards.sort(key=operator.itemgetter(2), reverse=True)
    return all_guards[0][0], all_guards[0][1]


timepoints = create_timepoints("inputs/input04.txt")
timepoints = to_intervals(timepoints)  # for every guard
days = [Day(timepoint) for timepoint in timepoints]

guard_id = find_sleepiest_guard(days)
minute_id = find_most_common_minute(days, guard_id)

minute_alt, guard_alt = find_highest_resting_guard_for_any_minute(days)

print(guard_id * minute_id, guard_alt * minute_alt)
