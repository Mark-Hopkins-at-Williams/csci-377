import math
import cnf
import copy
from util import irange, all_pairs_from_seq
from cnf import Cnf

class SudokuBoard:
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.cell_width = int(math.sqrt(len(self.matrix)))
        err = "Improper dimensions for a Sudoku board!"
        assert self.cell_width == math.sqrt(len(self.matrix)), err
        
    def __str__(self):
        row_strs = [''.join([str(digit) for digit in row]) for row in self.matrix]        
        return '\n'.join(row_strs)
 
    def rows(self):
        def row_cells(i, row_length):
            return [(i, j) for j in irange(1, row_length)]
        num_symbols = self.cell_width * self.cell_width
        return [row_cells(row, num_symbols) for row in irange(1, num_symbols)]
    
    def columns(self):
        def col_cells(j, col_length):
            return [(i, j) for i in irange(1, col_length)]
        num_symbols = self.cell_width * self.cell_width
        return [col_cells(col, num_symbols) for col in irange(1, num_symbols)]
 
    def zones(self):
        def zone_cells(a, b, cell_width):
            return [(i+1,j+1) for i in range((a-1) * cell_width, a * cell_width)
                              for j in range((b-1) * cell_width, b * cell_width)]
        return [zone_cells(a, b, self.cell_width) for a in irange(1, self.cell_width)
                                                  for b in irange(1, self.cell_width)]
  
    def general_clauses(self):
        result = (exactly_one_clauses(self.rows(), self.cell_width) + 
                  exactly_one_clauses(self.columns(), self.cell_width) +
                  exactly_one_clauses(self.zones(), self.cell_width) +
                  no_zero_cell_clauses(self.cell_width))
        return [cnf.c(clause) for clause in result]
 
    def cnf(self):
        clauses = self.general_clauses()
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                digit = self.matrix[row][col]
                if digit != 0:
                    clause = cnf.c(lit(digit, row+1, col+1))
                    clauses.append(clause)
        return Cnf(clauses)
    
    def solve(self, solver):
        model = solver(self.cnf())
        if model is None:
            return None
        matrix = copy.deepcopy(self.matrix)
        positive_literals = [l for l in model if model[l] == 1]
        for l in positive_literals:
            d, i, j, _ = interpret_lit(l)
            matrix[int(i)-1][int(j)-1] = int(d)
        return SudokuBoard(matrix)
                            
def lit(d, i, j, negate = False):
    # i.e. true when space (i, j) contains digit d
    literal = 'd{}_{}_{}'.format(d, i, j)
    if negate:
        literal = '!{}'.format(literal)
    return literal

def interpret_lit(l):
    negate = (l[0] == "!")
    if negate:
        l = l[2:]
    else:
        l = l[1:]
    d, i, j = l.split("_")
    return d, i, j, negate

def at_least_clause(cells, d):
    """
    Encodes: "The following cells have at least 1 of digit d."

    """  
    literals = [lit(d, i, j) for (i, j) in cells]
    return ' || '.join(literals)  

def at_most_clauses(cells, d):
    """
    Encodes: "The following cells have at most 1 of digit d."

    """ 
    clauses = []         
    for cell1, cell2 in all_pairs_from_seq(cells):
        clauses.append('{} || {}'.format(lit(d, cell1[0], cell1[1], negate=True), 
                                         lit(d, cell2[0], cell2[1], negate=True)))        
    return clauses

def exactly_one_clauses(groups, cell_width):
    clauses = []
    num_symbols = cell_width * cell_width
    for group in groups:
        for digit in irange(1, num_symbols):
            clauses.append(at_least_clause(group, digit))
            clauses += at_most_clauses(group, digit)
    return clauses
    
def no_zero_cell_clauses(cell_width):
    def no_zero_cells(i, j, row_length):
        """
        Encodes: "Cell i, j is non-zero."
    
        """ 
        literals = [lit(d, i, j) for d in irange(1, row_length)]
        return ' || '.join(literals)         
    row_length = cell_width * cell_width
    clauses = []
    for row in irange(1, row_length):
        for col in irange(1, row_length): 
            clauses.append(no_zero_cells(row, col, row_length))
    return clauses
                

