from collections import deque
from aoc09a import get_input


def game(num_players: int, last_marble: int) -> int:
    marbles = deque([0, 1])
    player = 1
    scores = [0] * num_players

    for marble in range(2, last_marble + 1):
        if marble % 23:
            marbles.rotate(2)
            marbles.append(marble)
        else:
            marbles.rotate(-7)
            second_marble = marbles.pop()
            scores[player - 1] += (marble + second_marble)
        player = (player + 1) % num_players
    print(max(scores))


if __name__ == '__main__':
    players, marbles = get_input("inputs/input09.txt")
    game(players, marbles*100)
