def get_difference(string1, string2):
    N = len(string1) # strings of same size
    index = -1
    for i in range(0, N):
        if string1[i] != string2[i]:
            if index != -1:
                return -1
            else:
                index = i
    return index


def get_appropriate_ID(filename):
    box_ids = [x.strip() for x in open(filename, "r").readlines()]
    for i in range(0, len(box_ids)-1):
        for j in range(i+1, len(box_ids)):
            first = box_ids[i]
            second = box_ids[j]
            diff = get_difference(first, second)
            if diff != -1:
                print(first[:diff] + first[diff+1:])


get_appropriate_ID("inputs/input02.txt")
