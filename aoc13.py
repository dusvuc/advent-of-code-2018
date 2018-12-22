from enum import Enum


class TileType(Enum):
    NONE = 0,
    HORIZONTAL = 1,
    VERTICAL = 2,
    INTERSECTION = 3,
    CURVE_FORWARD_SLASH = 4,
    CURVE_BACKWARD_SLASH = 5


class CartDirection(Enum):
    UP = 0,
    DOWN = 1,
    LEFT = 2,
    RIGHT = 3


class NextItem:

    def __init__(self, items):
        self.items = items
        self.size = len(items)
        self.current = 0

    def next(self):
        val = self.items[self.current]
        self.current = (self.current + 1) % self.size
        return val


class CartTurning:
    TOTAL_DIRECTIONS = 4

    __orientation = {
        CartDirection.UP: 0,
        CartDirection.RIGHT: 1,
        CartDirection.DOWN: 2,
        CartDirection.LEFT: 3
    }

    __decision = {v: k for k, v in __orientation.items()}

    def __init__(self):
        self.__current_value = 0
        self.swerve = NextItem([-1, 0, 1])

    def next_direction(self, current_direction: CartDirection):
        side = (self.swerve.next() + CartTurning.__orientation[current_direction]) % CartTurning.TOTAL_DIRECTIONS
        decision = CartTurning.__decision[side]
        return decision


class Tile:
    __translation = {
        '-': TileType.HORIZONTAL,
        '>': TileType.HORIZONTAL,
        '<': TileType.HORIZONTAL,
        '|': TileType.VERTICAL,
        '^': TileType.VERTICAL,
        'v': TileType.VERTICAL,
        '+': TileType.INTERSECTION,
        '/': TileType.CURVE_FORWARD_SLASH,
        '\\': TileType.CURVE_BACKWARD_SLASH,
        ' ': TileType.NONE
    }

    __inv_translation = {v: k for k, v in __translation.items()}

    def __init__(self, x: int, y: int, val: str):
        self.x = x
        self.y = y
        self.val = val
        self.type = Tile.__translation[val]

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)


class Cart:
    cart_id = 0

    __translation = {
        '^': CartDirection.UP,
        "v": CartDirection.DOWN,
        "<": CartDirection.LEFT,
        ">": CartDirection.RIGHT
    }

    __direction_change_backward = {
        CartDirection.LEFT: CartDirection.UP,
        CartDirection.UP: CartDirection.LEFT,
        CartDirection.DOWN: CartDirection.RIGHT,
        CartDirection.RIGHT: CartDirection.DOWN
    }

    __direction_change_forward = {
        CartDirection.LEFT: CartDirection.DOWN,
        CartDirection.DOWN: CartDirection.LEFT,
        CartDirection.UP: CartDirection.RIGHT,
        CartDirection.RIGHT: CartDirection.UP
    }

    def __init__(self, x: int, y: int, val: str):
        self.cart_id = Cart.cart_id
        Cart.cart_id += 1
        self.x = x
        self.y = y
        self.direction = Cart.__translation[val]
        self.turning = CartTurning()

    def __left(self):
        self.y -= 1

    def __right(self):
        self.y += 1

    def __up(self):
        self.x -= 1

    def __down(self):
        self.x += 1

    def move_horizontal(self):
        if self.direction == CartDirection.RIGHT:
            self.__right()
        else:
            self.__left()

    def move_vertical(self):
        if self.direction == CartDirection.UP:
            self.__up()
        else:
            self.__down()

    def move(self):
        if self.direction == CartDirection.UP or self.direction == CartDirection.DOWN:
            self.move_vertical()
        else:
            self.move_horizontal()

    def tick(self, tiles):
        tile = tiles[self.x][self.y]
        if tile.type == TileType.INTERSECTION:
            self.direction = self.turning.next_direction(self.direction)
        elif tile.type == TileType.CURVE_BACKWARD_SLASH:
            self.direction = Cart.__direction_change_backward[self.direction]
        elif tile.type == TileType.CURVE_FORWARD_SLASH:
            self.direction = Cart.__direction_change_forward[self.direction]
        elif tile.type == TileType.NONE:
            raise Exception("Stepped on none!")
        self.move()

    @staticmethod
    def is_cart(character: str) -> bool:
        return character in Cart.__translation

    def __repr__(self):
        return "({}, {}): {}".format(self.y, self.x, self.direction)

    def __lt__(self, other):
        if self.y == other.y:
            return self.x.__lt__(other.x)
        return self.y.__lt__(other.y)


def create_grid_and_carts(filename):
    lines = [line.rstrip() for line in open(filename) if line.strip()]
    mine = []
    carts = []
    for x in range(len(lines)):
        line = lines[x]
        mine_row = []
        mine.append(mine_row)
        for y in range(len(line)):
            character = line[y]
            mine_row.append(Tile(x, y, character))
            if Cart.is_cart(character):
                carts.append(Cart(x, y, character))
    return mine, carts


def check_for_collision(carts, cart):
    for cart_test in carts:
        if cart_test.cart_id != cart.cart_id and cart_test.x == cart.x and cart_test.y == cart.y:
            return cart_test.y, cart_test.x
    return None

def check_for_collision_id(carts, cart):
    for cart_test in carts:
        if cart_test.cart_id != cart.cart_id and cart_test.x == cart.x and cart_test.y == cart.y:
            return cart_test.cart_id, cart.cart_id
    return None


def run_carts(filename):
    mine, carts = create_grid_and_carts(filename)
    while True:
        carts.sort()

        for cart in carts:
            cart.tick(mine)
            if check_for_collision(carts, cart):
                return check_for_collision(carts, cart)


def run_carts_with_collisions(filename):
    mine, carts = create_grid_and_carts(filename)
    while True:
        carts.sort()

        to_remove = []
        for cart in carts:
            cart.tick(mine)
            if check_for_collision(carts, cart):
                to_remove.extend(check_for_collision_id(carts, cart))
        for cart_id in to_remove:
            carts = list(filter(lambda c: c.cart_id != cart_id, carts))
            if len(carts) == 1:
                return carts[0].y, carts[0].x



if __name__ == '__main__':
    filename = "inputs/input13.txt"
    print(run_carts(filename))
    print(run_carts_with_collisions(filename))
