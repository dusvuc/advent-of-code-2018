def get_counts(box_id):
    box_counts = dict()
    for letter in box_id.strip():
        if letter in box_counts:
            box_counts[letter] += 1
        else:
            box_counts[letter] = 1
    return box_counts


def has_letters(box_counts, num_letters):
    for values in box_counts.values():
        if values == num_letters:
            return True
    return False


def has_two_letters(counts):
    return has_letters(counts, 2)


def has_three_letters(counts):
    return has_letters(counts, 3)


def get_checksum(filename):
    box_ids = open(filename, "r").readlines()
    id_counts = [get_counts(box_id) for box_id in box_ids]

    num_two_letters, num_three_letters = 0, 0
    for id_count in id_counts:
        if has_two_letters(id_count):
            num_two_letters += 1
        if has_three_letters(id_count):
            num_three_letters += 1

    return num_two_letters * num_three_letters


checksum = get_checksum("inputs/input02.txt")
print(checksum)


