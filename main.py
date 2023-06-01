import pygame


class Variable:
    def __init__(self, row: int, column: int, domain: list, value: int | None):
        self.row = row
        self.column = column
        self.domain = domain
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Variable) and self.row == other.row and self.column == other.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))


WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)

grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def escape():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return


def DrawGrid():
    win = pygame.display.set_mode((WIDTH, WIDTH))
    win.fill(background_color)
    my_font = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] != 0:
                value = my_font.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

    pygame.display.update()

    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 6)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 6)

        pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()


def generate_variables() -> list:
    variables = []
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            variables.append(Variable(i, j, [x for x in range(1, len(grid) + 1)] if value == 0 else [value], None))
    return variables


def check_consistency(variables: list) -> bool:
    # Alldif global constraint
    for row in range(len(grid)):
        values = list(map(lambda x: x.value, filter(lambda x: x.row == row and x.value is not None, variables)))
        if not len(values) == len(set(values)):
            return False
    for col in range(len(grid)):
        values = list(map(lambda x: x.value, filter(lambda x: x.column == col and x.value is not None, variables)))
        if not len(values) == len(set(values)):
            return False
    return True


def select_unassigned_variable(variables: list) -> Variable:
    for i in variables:
        if i.value is None:
            return i


def check_complete(variables: list) -> bool:
    for i in variables:
        if i.value is None:
            return False
    return True


def backtrack(variables: list) -> bool:
    if check_complete(variables):
        return True
    var = select_unassigned_variable(variables)
    for i in var.domain:
        var.value = i
        if check_consistency(variables):
            result = backtrack(variables)
            if result:
                return True
        var.value = None
    return False


def get_variables_in_row(row: int, variables: list) -> list:
    return list(filter(lambda x: x.row == row, variables))


def get_variables_in_column(column: int, variables: list) -> list:
    return list(filter(lambda x: x.column == column, variables))


def generate_arcs(var: Variable, variables: list) -> set:
    row_constraints = get_variables_in_row(var.row, variables)
    col_constraints = get_variables_in_column(var.column, variables)
    arcs = set()
    for i, j in zip(row_constraints, col_constraints):
        if not i == var:
            arcs.add((var, i))
        if not j == var:
            arcs.add((var, j))
    return arcs


def satisfy_constraints(a: int, b: int) -> bool:
    return not a == b


def revise(v1: Variable, v2: Variable) -> bool:
    revised = False
    for i in v1.domain:
        satisfy = False
        for j in v2.domain:
            if satisfy_constraints(i, j):
                satisfy = True
                break
        if not satisfy:
            v1.domain.remove(i)
            revised = True
    return revised


def ac3(variables: list) -> bool:
    # Create a queue of arcs
    queue = []
    for i in variables:
        queue.extend(generate_arcs(i, variables))
    # Reduce domains before start searching
    while len(queue) > 0:
        arc = queue.pop(0)
        if revise(*arc):
            if len(arc[0].domain) == 0:
                return False
            queue.extend(generate_arcs(arc[0], variables) - {arc})
    return True


def solver():
    variables = generate_variables()
    if not ac3(variables):
        return False
    result = backtrack(variables)
    if result:
        for i in variables:
            grid[i.row][i.column] = i.value


def main():
    pygame.font.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("CH02")
    win.fill(background_color)
    solver()
    DrawGrid()
    while True:
        escape()


if __name__ == '__main__':
    main()
