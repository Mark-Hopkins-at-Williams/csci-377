import math
import cnf

class SudokuBoard:
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.cell_width = int(math.sqrt(len(self.matrix)))
        err = "Improper dimensions for a Sudoku board!"
        assert self.cell_width == math.sqrt(len(self.matrix)), err
        
    def __str__(self):
        row_strs = []
        for row in self.matrix:
            row_str = ''.join([str(digit) for digit in row])
            row_strs.append(row_str)
        return '\n'.join(row_strs)
    
    def cnf(self):
        clauses = general_clauses(self.cell_width)
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                digit = self.matrix[row][col]
                if digit != 0:
                    clause = cnf.c(lit(digit, row+1, col+1))
                    clauses.append(clause)
        return clauses
                    
board0 = SudokuBoard([[0, 0, 0, 3], [0, 0, 0, 2], [3, 0, 0, 0], [4, 0, 0, 0]])
board1 = SudokuBoard([[0, 3, 0, 3], [0, 0, 0, 2], [3, 0, 0, 0], [4, 0, 0, 0]])

def general_clauses(cell_width = 2):
    result = (general_row_clauses(cell_width) + 
              general_col_clauses(cell_width) +
              general_zone_clauses(cell_width))
    return [cnf.c(clause) for clause in result]


def irange(i, j):
    return range(i, j+1)
        
def lit(d, i, j, negate = False):
    # i.e. true when space (i, j) contains digit d
    literal = 'd{}_{}_{}'.format(d, i, j)
    if negate:
        literal = '!{}'.format(literal)
    return literal
    
def all_pairs(i, j):
    for a in irange(i, j):
        for b in irange(a+1, j):
            yield (a, b)

def all_pairs_from_seq(seq):
    for a in range(len(seq)):
        for b in range(a+1, len(seq)):
            yield seq[a], seq[b]


def general_row_clauses(cell_width = 2):
    clauses = []
    num_symbols = cell_width * cell_width
    for digit in irange(1, num_symbols):
        for row in irange(1, num_symbols):            
            clauses.append(row_at_least_clause(row, digit, num_symbols))
            clauses += row_at_most_clauses(row, digit, num_symbols)
    return clauses
            
def row_at_least_clause(i, d, row_length):
    """
    Encodes: "Row i has at least 1 of digit d."

    """
    literals = [lit(d, i, j) for j in irange(1, row_length)]
    return ' || '.join(literals)        

def row_at_most_clauses(i, d, row_length):
    """
    Encodes: "Row i has at most 1 of digit d."

    """ 
    clauses = []         
    for (a, b) in all_pairs(1, row_length):
        clauses.append('{} || {}'.format(lit(d, i, a, negate=True), 
                                         lit(d, i, b, negate=True)))        
    return clauses
    
def general_col_clauses(cell_width = 2):
    clauses = []
    num_symbols = cell_width * cell_width
    for digit in irange(1, num_symbols):
        for col in irange(1, num_symbols):            
            clauses.append(col_at_least_clause(col, digit, num_symbols))
            clauses += col_at_most_clauses(col, digit, num_symbols)
    return clauses
            
def col_at_least_clause(j, d, col_length):
    """
    Encodes: "Column j has at least 1 of digit d."

    """
    literals = [lit(d, i, j) for i in irange(1, col_length)]
    return ' || '.join(literals)  
    
def col_at_most_clauses(j, d, col_length):
    """
    Encodes: "Column j has at most 1 of digit d."

    """ 
    clauses = []         
    for (a, b) in all_pairs(1, col_length):
        clauses.append('{} || {}'.format(lit(d, a, j, negate=True), 
                                         lit(d, b, j, negate=True)))        
    return clauses

def general_zone_clauses(cell_width = 2):
    clauses = []
    num_symbols = cell_width * cell_width
    for digit in irange(1, num_symbols):
        for a in irange(1, cell_width):
            for b in irange(1, cell_width):
                clauses.append(zone_at_least_clause(a, b, digit, cell_width))
                clauses += zone_at_most_clauses(a, b, digit, cell_width)
    return clauses

def zone_cells(a, b, cell_width):
    cells = []
    for i in range((a-1) * cell_width, a * cell_width):
        for j in range((b-1) * cell_width, b * cell_width):
            cells.append((i+1,j+1))
    return cells

def zone_at_least_clause(a, b, d, cell_width):
    """
    Encodes: "Zone (a, b) has at least 1 of digit d."

    """    
    literals = [lit(d, i, j) for (i, j) in zone_cells(a, b, cell_width)]
    return ' || '.join(literals)  
    
def zone_at_most_clauses(a, b, d, cell_width):
    """
    Encodes: "Zone (a, b) has at most 1 of digit d."

    """ 
    clauses = []         
    for cell1, cell2 in all_pairs_from_seq(zone_cells(a, b, cell_width)):
        clauses.append('{} || {}'.format(lit(d, cell1[0], cell1[1], negate=True), 
                                         lit(d, cell2[0], cell2[1], negate=True)))        
    return clauses
    


        