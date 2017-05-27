assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

boxes = cross(rows, cols)

# each unit can only contain a single instance of each number
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_unit_1 = [[s[0]+s[1] for s in zip(rows, cols)]]
diag_unit_2 = [[s[0]+s[1] for s in zip(rows[::-1], cols)]]

# list of all units to iterate over
unitlist = row_units + column_units + square_units + diag_unit_1 + diag_unit_2

# helper for peers
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)

# the peers of a particular box given the units it is a part of
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        #find boxes with two possible values
        gen1 = [box for box in unit if len(values[box]) == 2]
        for twin1 in gen1:
            gen2 = [box for box in gen1 if box != twin1]
            for twin2 in gen2:
                # if the values of the two twins match, then these are true naked twins
                if values[twin1] == values[twin2]:
                    for peer in unit:
                        # eliminate the value of the twins from all other peers
                        if peer == twin1 or peer == twin2:
                            continue;
                        values[peer] = values[peer].replace(values[twin1][0], '')
                        values[peer] = values[peer].replace(values[twin1][1], '')
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
	    Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    for c in grid:
        if c == '.':
            chars.append('123456789')
        else:
            chars.append(c)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # width of the puzzle
    width = max(len(values[s]) for s in boxes) + 1

    # the line to be printed by this function
    line = '+'.join(['-'*(width*3)]*3)

    # print the possbiel values of each box in each row
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print (line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for box in values:
        if len(values[box]) == 1:
            for peer in peers[box]:
                values[peer] = values[peer].replace(values[box], '')

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit;
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    # indicates that we cannot find a solution by elimination
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    #failure case:
    if values == False:
        return False

    # pass case:
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # recursive case:
    # Choose one of the unfilled squares with the fewest possibilities
    min_x = 10;
    boxen = []
    for box in values:
        if len(values[box]) < min_x and len(values[box]) > 1:
            boxen = []
            min_x = len(values[box])
            boxen.append(box)
        if len(values[box]) == min_x:
            boxen.append(box)
    # choose random box
    box_choice = boxen[0]
    # Now use recursion to solve each one of the resulting sudokus
    # if one returns a value (not False), return that answer!
    for val in values[box_choice]:
        new_values = values.copy()
        new_values[box_choice] = val;
        attempt = search(new_values)
        if(attempt):
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    attempt = reduce_puzzle(values)
    for box in attempt:
        if len(attempt[box]) != 1:
            return False
    return attempt

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
