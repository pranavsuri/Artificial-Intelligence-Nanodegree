assignments = []

class Sudoku():
    """Initializing and solving a classic/diagnol Sudoku.

    ATTRIBUTES:
        grid        : row-wise string representation of Sudoku
        row         : string 'ABCDEFGHI'
        cols        : string '123456789'
        boxes       : list of all squares
        unit_list   : list of all units
        peers       : dictionary of peers for each box
        values      : dictionary of box:digits
    """

    def __init__(self, grid, partial=False, diag=False,rows='ABCDEFGHI', cols='123456789'):
        """
            Args:
            - grid      : 81-char string to be solved if 'partial = False'
                          else intermediate solution as a dict of box:values
            - partial   : init with string or partial solution
            - diag      : boolean - diagonal Sudoku = True

            Returns:
                All class attributes initialized
        """
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.grid_init(partial, diag)

    def cross(self, A, B):
        """
        Cross product of elements in a and b
        """
        return [a+b for a in A for b in B]

    def assign_value(self, box, value):
        """Update the values dictionary.
        Assigns a value to a given box. If it updates the board, records it.
        """
        self.values[box] = value
        if len(value) == 1:
            assignments.append(self.values.copy())

    def grid_init(self, partial, diag):
        """Setup the grid and initialize difference parameters.
        i.e. Boxes, Values, Peers.
        """
        self.boxes = self.cross(self.rows,self.cols)

        if partial:
            self.values = self.grid.copy()
        else:
            self.values = {}
            for box,char in zip(self.boxes,self.grid):
                if char == '.':
                    self.values[box] = self.cols
                else:
                    self.values[box] = char

        rowunits = [self.cross(r,self.cols) for r in self.rows]
        colunits = [self.cross(self.rows,c) for c in self.cols]
        squareunits = [self.cross(rs, cs) for rs in ['ABC','DEF','GHI'] for cs in ['123','456','789']]

        self.unitlist = rowunits + colunits + squareunits
        if diag:
            self.unitlist += [[r+c for r,c in zip(self.rows,self.cols)],
                              [r+c for r,c in zip(self.rows,self.cols[::-1])]]

        units = {box:[u for u in self.unitlist if box in u] for box in self.boxes}
        self.peers = {box:set(sum(units[box],[]))-set([box]) for box in self.boxes}

    def display(self):
        """Display the values as a 2-D grid.
        Args:
            values(dict): The sudoku in dictionary form
        """
        width = 1+max(len(self.values[s]) for s in self.boxes)
        line = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(self.values[r+c].center(width)+('|' if c in '36' else '')
                      for c in self.cols))
            if r in 'CF': print(line)
        print('\n')

    def solved_values(self):
        return [box for box in self.boxes if len(self.values[box]) == 1]

    def eliminate(self):
        """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single
        value, eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form
        Returns:
            Resulting Sudoku in dictionary form after eliminating values
        """
        solved_values_boxes = self.solved_values()
        for box in solved_values_boxes:
            digit = self.values[box]
            for peer in self.peers[box]:
                value = self.values[peer]
                value = value.replace(digit,'')
                self.assign_value(peer, value)

    def only_choice(self):
        """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only
        choices.
        """
        for unit in self.unitlist:
            for digit in self.cols:
                boxes_containing_digit =[box for box in unit if digit in self.values[box]]
                if len(boxes_containing_digit) == 1:
                    self.assign_value(boxes_containing_digit[0], digit)

    #Naked-Twins Stragtegy
    def find_naked_twins(self):
        twins = [[a for a in u
                        for b in u
                            if (a != b) and (len(self.values[a]) == 2)
                                        and (self.values[a] == self.values[b])
                 ]
                 for i,u in enumerate(self.unitlist)
                ]
        return twins

    def eliminate_naked_twins(self, twins):
        for i, twin in enumerate(twins):
            if twin:
                for box in self.unitlist[i]:
                    if box not in twin:
                        for digit in self.values[twin[0]]:
                            value = self.values[box]
                            if len(value) > 1 :
                                value = value.replace(digit,'')
                                self.assign_value(box, value)

    def naked_twins(self):
        """Eliminate values using the naked twins strategy.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}

        Returns:
            the values dictionary with the naked twins eliminated from peers.
        """
        #Find all instances of naked twins
        twins = self.find_naked_twins()
        #Eliminate the naked twins as possibilities for their units
        self.eliminate_naked_twins(twins)

    def reduce_puzzle(self):
        """Iterate eliminate() and only_choice().
        If at some point, there is a box with no available values, return False.

        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same,
        return the sudoku.

        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
        """
        stalled = False
        while not stalled:
            solved_values_before = self.solved_values()
            self.eliminate()
            self.only_choice()
            solved_values_after = self.solved_values()

            stalled = solved_values_before == solved_values_after

            if len([box for box in self.boxes if len( self.values[box]) == 0]):
                # if it is still solvable run naked_twins or not
                self.naked_twins()
                return True
        return False

    def search(self):
        """Using depth-first search and propagation,
        create a search tree and solve the sudoku.
        """
        # Reduce the puzzle
        failed = self.reduce_puzzle()
        if failed :
            return False #Tree-leaf: not a solution
        if all(len(self.values[box]) == 1 for box in self.boxes):
            return True #Solved

        # Choose box with min possibilities
        n, box = min((len(self.values[box]),box) for box in self.boxes if len(self.values[box]) > 1)

        # Recursion to solve each one of the resulting sudokus,
        # and if one returns a value (not False), return that answer!
        for digit in self.values[box]:
            tmp = self.values.copy() # copy of the values in case of failure = 'attempt ===False'
            self.values[box] = digit
            attempt = self.search()
            if attempt:
                return attempt
            else:
                self.values = tmp
