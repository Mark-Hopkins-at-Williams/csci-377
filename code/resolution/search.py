from cnf import Clause, Literal
from resolution import unit_resolution
   
class SearchSolver:
            
    def __call__(self, sent):
        symbols = sent.get_symbols()
        self.visited = 0
        result = self._search_solver_helper(sent, symbols)
        return result
    
    def _search_solver_helper(self, sent, symbols):
        def assign(model_so_far, symbol, bool_assignment):
            if bool_assignment:
                assignment = 1
            else:
                assignment = -1
            return {**model_so_far, symbol: assignment}
        
        self.visited += 1
        if sent is None:
            return None
        m = sent.current_assignment()
        unassigned_symbols = sorted(symbols - m.keys())  # TODO: different orders
        if len(unassigned_symbols) == 0:
            if sent.check_term(m):
                return m
            else:
                return None
        else:
            next_symbol = unassigned_symbols[0]
            positive_unit_clause = Clause([Literal(next_symbol, neg=False)])
            new_clauses = unit_resolution(positive_unit_clause, sent)
            sat_if_true = self._search_solver_helper(new_clauses, symbols) 
            if sat_if_true != None: # early termination if already satisfied
                return sat_if_true
            negative_unit_clause = Clause([Literal(next_symbol, neg=True)])
            new_clauses = unit_resolution(negative_unit_clause, sent)
            sat_if_false =  self._search_solver_helper(new_clauses, symbols)
            return sat_if_false       
    


