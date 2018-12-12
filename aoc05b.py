import operator
from aoc05a import react_polymer

line = open("inputs/input05.txt").readlines()[0].strip()

all_letters = set()
for letter in line:
    all_letters.add(letter.lower())


def remove_letter(line, letter):
    temp_line = line.replace(letter.lower(), "")
    temp_line = temp_line.replace(letter.upper(), "")
    return temp_line


changed = {x: remove_letter(line, x) for x in all_letters}
counts = [len(react_polymer(line)) for line in changed.values()]
print(min(counts))
