import re


def get_input(filename):
    line = open(filename, mode="r").readline().strip()
    regex = re.compile("(\d*) players; last marble is worth (\d*) points")
    groups = regex.match(line).groups()
    return int(groups[0]), int(groups[1])


def game(num_players: int, last_marble: int) -> int:
    current = 1
    marbles = [0, 1]
    player = 1
    scores = [0] * num_players


    for marble in range(2, last_marble + 1):
        if marble % 23:
            index = (current + 2) % len(marbles)
            if index:
                marbles.insert(index, marble)
                current = index
            else:
                marbles.append(marble)
                current = len(marbles) - 1
        else:
            index -= 7
            index = index % len(marbles)
            second_marble = marbles.pop(index)
            current = index
            scores[player - 1] += (marble + second_marble)
        player = (player + 1) % num_players
    print(max(scores))


if __name__ == '__main__':
    players, marbles = get_input("inputs/input09.txt")
    game(players, marbles)
