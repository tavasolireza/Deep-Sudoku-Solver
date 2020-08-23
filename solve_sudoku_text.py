rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
unit_list = row_units + column_units + square_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)


def display(sudoku_values):
    width = 1 + max(len(sudoku_values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3) + '-'] * 3)
    for r in rows:
        print(' ', end='')
        print(''.join(sudoku_values[r + c].center(width) + ('| ' if (c == '3' or c == '6') else '') for c in cols))
        if r == 'C' or r == 'F':
            print(line)
    return


def grid_values(grid):
    chars = []
    digits = '123456789'
    for box in grid:
        if box in digits:
            chars.append(box)
        if box == '.':
            chars.append(digits)
    if len(chars) == 81:
        return dict(zip(boxes, chars))


def eliminate(sudoku_values):
    solved_values = [box for box in sudoku_values.keys() if len(sudoku_values[box]) == 1]
    for box in solved_values:
        digit = sudoku_values[box]
        for peer in peers[box]:
            sudoku_values[peer] = sudoku_values[peer].replace(digit, '')
    return sudoku_values


def only_choice(sudoku_values):
    for unit in unit_list:
        for digit in '123456789':
            only_choice_box = [box for box in unit if digit in sudoku_values[box]]
            if len(only_choice_box) == 1:
                sudoku_values[only_choice_box[0]] = digit
    return sudoku_values


def reduce_puzzle(sudoku_values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in sudoku_values.keys() if len(sudoku_values[box]) == 1])
        sudoku_values = only_choice(eliminate(sudoku_values))
        solved_values_after = len([box for box in sudoku_values.keys() if len(sudoku_values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in sudoku_values.keys() if len(sudoku_values[box]) == 0]):
            return False
    return sudoku_values


def search(sudoku_values):
    sudoku_values = reduce_puzzle(sudoku_values)
    if sudoku_values is False:
        return False
    if all(len(sudoku_values[s]) == 1 for s in boxes):
        return sudoku_values
    n, s = min((len(sudoku_values[s]), s) for s in boxes if len(sudoku_values[s]) > 1)
    for value in sudoku_values[s]:
        new_sudoku = sudoku_values.copy()
        new_sudoku[s] = value
        solved_sudoku = search(new_sudoku)
        if solved_sudoku:
            return solved_sudoku
