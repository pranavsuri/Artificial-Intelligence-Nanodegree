import sudoku as sdk

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form
        {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    sudoku = sdk.Sudoku(values, partial=True)
    sudoku.naked_twins()

    return sudoku.values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    diagonal_sudoku = sdk.Sudoku(grid, diag=True)
    diagonal_sudoku.search()
    diagonal_sudoku.display()

    return diagonal_sudoku.values

if __name__ == '__main__':
    diag_sudoku_grid = '9...6...7.6.971.4...........5.....3.41.....28.7.....6...........9.854.7.5...1...4'
    solve(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(sdk.assignments)

    except SystemExit:
        pass
    except:
        print('Could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
