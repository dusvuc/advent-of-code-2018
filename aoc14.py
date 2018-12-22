class Elf:
    def __init__(self, start_value, start_position):
        self.current_value = start_value
        self.current_position = start_position

    def step(self, recipes):
        self.current_position = (self.current_position + self.current_value + 1) % len(recipes)
        self.current_value = recipes[self.current_position]


def get_new_recipes(new_recipe):
    return [int(letter) for letter in str(new_recipe)]


def get_recipes(filename: str):
    first_elf = Elf(3, 0)
    second_elf = Elf(7, 1)
    recipes = [3, 7]

    needed = int(open(filename).readline().strip())
    while len(recipes) < needed + 10:
        new_recipe = first_elf.current_value + second_elf.current_value
        new_recipes = get_new_recipes(new_recipe)
        recipes.extend(new_recipes)
        first_elf.step(recipes)
        second_elf.step(recipes)

    return "".join([str(x) for x in recipes[needed: needed + 10]])


def get_preceding_recipes(filename: str):
    first_elf = Elf(3, 0)
    second_elf = Elf(7, 1)
    recipes = [3, 7]
    recipes_text = "37"

    needed = "503761"
    offset = 0
    while True:
        new_recipe = first_elf.current_value + second_elf.current_value
        new_recipes = get_new_recipes(new_recipe)
        recipes.extend(new_recipes)
        recipes_text += "".join([str(x) for x in new_recipes])
        first_elf.step(recipes)
        second_elf.step(recipes)

        val = recipes_text.find(str(needed))
        if val != -1:
            return len(recipes_text[:val]) + offset
        else:
            recipes_len = len(recipes_text)
            if recipes_len > 6:
                recipes_text = recipes_text[recipes_len-6:]
                offset += recipes_len-6



filename = "inputs/input14.txt"
print(get_recipes(filename))
print(get_preceding_recipes(filename))
