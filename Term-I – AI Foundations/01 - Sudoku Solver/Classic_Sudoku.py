#Row-Column Labels
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    """Make 2-char combos from two strings.
    Arguments: Two strings
    """
    return [s+t for s in a for t in b]

#Defining Boxes
boxes = cross(rows, cols)

#Defining Units
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

#Testing Example
#grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_values_unsolved(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Arguments:
        grid: Sudoku grid in string form, 81 characters long

    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty
    """
    assert(len(grid)==81)
    return dict(zip(boxes, grid))

def display(values):
    """Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty
    """
    values = []
    all_digits = '123456789'
    for n in grid:
        if n == '.':
            values.append(all_digits)
        elif n in all_digits:
            values.append(n)

    assert len(values)==81
    return dict(zip(boxes, values))

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form
    Returns:
        Resulting Sudoku in dictionary form after eliminating values
    """
    #This will create a list of boxes that are solved
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """Iterate eliminate() and only_choice().
    If at some point, there is a box with no available values, return False.

    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        #Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        #Use the Eliminate Strategy
        values = eliminate(values)
        #Use the Only Choice Strategy
        values = only_choice(values)
        #Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        #If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        #Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search_puzzle(values):
    """Using depth-first search and propagation,
    create a search tree and solve the sudoku."""

    #Reduce the puzzle
    values = reduce_puzzle(values)
    if values is False:
        return False ##Failed early
    if all(len(values[s]) == 1 for s in boxes):
        return values ##Solved!

    #Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    #print(n,s)

    #Recursion to solve each one of the resulting sudokus,
    #and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

if __name__ == '__main__':
    #Testing Example
    print("Enter the Sudoku values row-wise.\n\nAn example is given below:")
    print('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..\n')
    grid = input("Enter the Sudoku string:\n")
    print('\n')
    display(grid_values_unsolved(grid))
    print("\n")
    display(search_puzzle(reduce_puzzle(grid_values(grid))))
