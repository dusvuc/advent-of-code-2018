def game(num_players: int, last_marble: int) -> int:
    current = 1
    marbles = [0, 1]
    player = 1
    scores = [0] * num_players
    print(scores)

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


game(493, 71863)
