def get_int(line):
    sign = line[0]
    val = int(line[1:])
    val = val if sign == "+" else -val
    return val


def find_frequency():
    shifts = [get_int(x) for x in open("inputs/input01.txt", "r").readlines()]
    frequencies = [0]
    frequency = 0
    while True:
        for shift in shifts:
            frequency += shift
            if frequency in frequencies:
                return frequency
            else:
                frequencies.append(frequency)


res = find_frequency()
print(res)
