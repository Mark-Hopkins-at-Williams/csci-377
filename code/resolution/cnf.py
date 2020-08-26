
def l(s):
    if s[0] == '!':
        return Literal(s[1:], True)
    else:
        return Literal(s, False)

def c(s):
    """
    Convenience method for constructing CNF clauses, e.g. for Exercise 7.12:
    
    c0 = c('a || b') 
    c1 = c('!a || b || e')        
    c2 = c('a || !b')        
    c3 = c('b || !e')        
    c4 = c('d || !e')        
    c5 = c('!b || !c || !f')        
    c6 = c('a || !e')        
    c7 = c('!b || f')        
    c8 = c('!b || c')        
    
    """
    if s == 'FALSE':
        literal_strings = []
    else:
        literal_strings = [x.strip() for x in s.split('||')]
    return Clause([l(x) for x in literal_strings])

def sentence(s):
    return Cnf([c(clause) for clause in s])


class Literal:
    def __init__(self, symbol, neg=False):
        self.symbol = symbol
        self.neg  = neg
    
    def __eq__(self, other):
        return self.symbol == other.symbol and self.neg == other.neg

    def __hash__(self):
        return hash(self.symbol) + hash(self.neg)
    
    def __str__(self):
        result = ''
        if self.neg:
            result = '!'
        return result + self.symbol
 
class Clause:
    def __init__(self, literals):
        self.literals = literals
        self.literal_values = dict()
        for lit in self.literals:
            self.literal_values[lit.symbol] = lit.neg

    def __len__(self):
        return len(self.literals)

    def __bool__(self):
        return len(self.literals) > 0

    def __eq__(self, other):
        return set(self.literals) == set(other.literals)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        return hash(tuple(sorted([str(l) for l in self.literals])))

    def __str__(self):
        if len(self.literals) == 0:
            return 'FALSE'
        else:
            return ' || '.join([str(l) for l in self.literals])
        
    def __contains__(self, sym):
        return sym in self.literal_values

    def __or__(self, other):
        common_symbols = set(self.literal_values.keys()) & set(other.literal_values.keys())
        for sym in common_symbols:
            if self.literal_values[sym] != other.literal_values[sym]:
                return None
        return Clause(list(set(self.literals + other.literals)))

    def __getitem__(self, sym):
        return self.literal_values[sym]

    def symbols(self):
        return set([l.symbol for l in self.literals])

    def remove(self, sym):
        new_literals = set(self.literals) - set([Literal(sym, False), Literal(sym, True)])
        return Clause(list(new_literals))


class Cnf:
    def __init__(self, clauses):
        self.clauses = clauses

 
    def check_term(self, term):
        def check_against_clause(clause):
            for symbol in clause.symbols():
                if term[symbol] == -1 and clause[symbol]: # TODO: fix this!
                    return True
                elif term[symbol] == 1 and not clause[symbol]: # TODO: fix this!
                    return True
            return False
        for clause in self.clauses:
            if not check_against_clause(clause):
                return False
        return True   

    def get_symbols(self):
        syms = set([])
        for clause in self.clauses:
            syms = syms | clause.symbols()
        return syms

    def current_assignment(self):
        def value(b):
            return 1 if b else -1  
        unit_clauses = [c.literals[0] for c in self.clauses if len(c) == 1]
        model = {c.symbol: value(not c.neg) for c in unit_clauses}
        return model
    
    def __str__(self):
        clause_strs = sorted([str(c) for c in self.clauses])     
        return '\n'.join(clause_strs)
    
    

