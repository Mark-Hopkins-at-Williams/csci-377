from cnf import Clause, Literal, get_symbols, check_term
from resolution import unit_resolution
   
class SearchSolver:
            
    def __call__(self, clauses):
        symbols = get_symbols(clauses)
        self.visited = 0
        result = self._search_solver_helper(clauses, symbols)
        return result
    
    def _search_solver_helper(self, clauses, symbols):
        def assign(model_so_far, symbol, bool_assignment):
            if bool_assignment:
                assignment = 1
            else:
                assignment = -1
            return {**model_so_far, symbol: assignment}

        def model_from_clauses(clauses):
            def value(b):
                return 1 if b else -1  
            unit_clauses = [c.literals[0] for c in clauses if len(c) == 1]
            model = {c.symbol: value(not c.neg) for c in unit_clauses}
            return model
        
        self.visited += 1
        if clauses is None:
            return None
        m = model_from_clauses(clauses)
        unassigned_symbols = sorted(symbols - m.keys())  # TODO: different orders
        if len(unassigned_symbols) == 0:
            if check_term(m, clauses):
                return m
            else:
                return None
        else:
            next_symbol = unassigned_symbols[0]
            positive_unit_clause = Clause([Literal(next_symbol, neg=False)])
            new_clauses = unit_resolution(positive_unit_clause, clauses)
            sat_if_true = self._search_solver_helper(new_clauses, symbols) 
            if sat_if_true != None: # early termination if already satisfied
                return sat_if_true
            negative_unit_clause = Clause([Literal(next_symbol, neg=True)])
            new_clauses = unit_resolution(negative_unit_clause, clauses)
            sat_if_false =  self._search_solver_helper(new_clauses, symbols)
            return sat_if_false       
    


