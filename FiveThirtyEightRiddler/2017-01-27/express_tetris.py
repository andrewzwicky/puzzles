from enum import Enum
import itertools
import copy


# shapes must be regularly sized
# each unique rotation has a separate entry here
class Shapes(Enum):
    L0 = [(True, False, False),
          (True, True, True)]
    L1 = [(False, True),
          (False, True),
          (True, True)]
    L2 = [(True, True, True),
          (False, False, True)]
    L3 = [(True, True),
          (True, False),
          (True, False)]
    J0 = [(True, True, True),
          (True, False, False)]
    J1 = [(True, False),
          (True, False),
          (True, True)]
    J2 = [(False, False, True),
          (True, True, True)]
    J3 = [(True, True),
          (False, True),
          (False, True)]
    O = [(True, True),
         (True, True)]
    I0 = [(True, True, True, True)]
    I1 = [(True,), (True,), (True,), (True,)]
    S0 = [(True, True, False),
          (False, True, True)]
    S1 = [(False, True),
          (True, True),
          (True, False)]
    Z0 = [(False, True, True),
          (True, True, False)]
    Z1 = [(True, False),
          (True, True),
          (False, True)]
    T0 = [(False, True, False),
          (True, True, True)]
    T1 = [(True, False),
          (True, True),
          (True, False)]
    T2 = [(False, True),
          (True, True),
          (False, True)]
    T3 = [(True, True, True),
          (False, True, False)]

# characters to differentiate shapes in the grid
characters = "*#+x%&"


def pack_shape(grid, shape, target_col, char_index):
    shape_height = len(shape.value)
    shape_width = len(shape.value[0])

    grid_height = len(grid)
    grid_width = len(grid[0])

    if shape_height > grid_height or shape_width > grid_width:
        return None

    if shape_width + target_col > grid_width:
        return None

    final_row = find_bottom_row(grid, shape, target_col)
    if final_row is None:
        return None

    if final_row + (shape_height - 1) < grid_height:
        output = copy.deepcopy(grid)
        for row, shape_row in enumerate(shape.value):
            for col, val in enumerate(shape_row):
                if val:
                    output[final_row + row][target_col + col] = characters[char_index]

        return output

    return None


def find_bottom_row(grid, shape, target_col):
    grid_height = len(grid)

    for this_row in reversed(range(grid_height)):
        for grid_row, shape_row in zip(grid[this_row:], shape.value):
            for g, s in zip(grid_row[target_col:], shape_row):
                if g and s:
                    result = this_row + 1
                    if result >= grid_height:
                        return None
                    else:
                        return result

    return 0


def covered(grid):
    for col in zip(*grid):
        false_found = False
        for row in col:
            if row is False:
                false_found = True
            if false_found and row is not False:
                return True

    return False


def recursive_pack(grid, filled_shapes):
    for shape in Shapes:
        try:
            column = grid[-1].index(False)
        except ValueError:
            column = None
        if column is not None:
            new_grid = pack_shape(grid, shape, column, len(filled_shapes))
            if new_grid is not None and not covered(new_grid):
                if all(itertools.chain.from_iterable(new_grid)):
                    yield new_grid
                else:
                    for g in recursive_pack(new_grid, filled_shapes + [(shape, column)]):
                        yield g


if __name__ == "__main__":
    width = 10
    height = 2
    grid = [[False for _ in range(width)] for _ in range(height)]

    count = 0
    for g in recursive_pack(grid, []):
        count += 1
        for line in reversed(g):
            print("".join(line))
        print(count)
