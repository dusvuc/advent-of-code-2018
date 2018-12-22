import numpy as np
import operator


def power_level(x, y, grid_serial):
    return power_level_shifted(x + 1, y + 1, grid_serial)


def power_level_shifted(x, y, grid_serial):
    rack_id = x + 10
    p_level = rack_id * y
    p_level += grid_serial
    p_level *= rack_id
    p_level = int(str(p_level)[-3]) if p_level >= 100 else 0
    p_level -= 5
    return p_level


def make_grid(grid_serial):
    grid = np.zeros((300, 300), dtype=np.int64)
    for i in range(0, 300):
        for j in range(0, 300):
            grid[i][j] = power_level(i, j, grid_serial)
    return grid


def grid_power_levels(grid, number):
    size = 300-number+1
    grid_vals = np.zeros((size, size), dtype=np.int64)
    for i in range(0, size):
        for j in range(0, size):
            grid_vals[i, j] = grid[i:i + number, j:j + number].sum()
    return grid_vals


def find_max(grid_levels):
    vals = np.unravel_index(np.argmax(grid_levels, axis=None), grid_levels.shape)
    return vals[0], vals[1]


def get_permutations(grid):
    data = []
    for i in range(1, 301):
        grid_levels = grid_power_levels(grid, i)
        index = find_max(grid_levels)
        val = grid_levels[index]
        data.append((index, val, i))
    data.sort(key=operator.itemgetter(1))
    return data



val = int(open("inputs/input11.txt").readline().strip())
grid = make_grid(8561)
data = get_permutations(grid)
print(data)
