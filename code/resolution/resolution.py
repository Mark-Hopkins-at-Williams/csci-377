import queue
from cnf import Cnf
from util import log

def resolve_symbol(clause1, clause2, symbol):
    if symbol in clause1 and symbol in clause2:
        if clause1[symbol] and not clause2[symbol]:
            return clause1.remove(symbol) | clause2.remove(symbol)
        if not clause1[symbol] and clause2[symbol]:
            return clause1.remove(symbol) | clause2.remove(symbol)
    return None

def resolve(clause1, clause2):
    resolvents = []
    for sym in clause1.symbols() & clause2.symbols():
       resolvent = resolve_symbol(clause1, clause2, sym)  
       if resolvent is not None:
           resolvents.append(resolvent)
    return resolvents

class ClauseQueue:
    def __init__(self, queue = queue.Queue(), priority_function = lambda clause: 0):
        self.queue = queue
        self.priority_function = priority_function
        self.cached_clauses = set([])
        
    def push(self, clause):
        if not clause in self.cached_clauses:
            self.queue.put((self.priority_function(clause), clause))
            self.cached_clauses.add(clause)
            return True
        else:
            return False
    
    def pop(self):
        return self.queue.get()[1]
    
    def empty(self):
        return self.queue.empty()
    
    def numGenerated(self):
        return len(self.cached_clauses)

def general_resolution_solver(processed, initial_unprocessed, clause_filter):
    unprocessed = ClauseQueue(queue.PriorityQueue(), lambda clause: len(clause))
    for c in initial_unprocessed:
        unprocessed.push(c)
    while not unprocessed.empty():
        next_to_process = unprocessed.pop()
        if clause_filter(next_to_process): 
            for clause in processed:
                for resolvent in resolve(next_to_process, clause):
                    is_new_clause = unprocessed.push(resolvent)
                    if is_new_clause:
                        log("{} [BY RESOLVING {} WITH {}]"
                            .format(resolvent, next_to_process, clause))                    
                    if not bool(resolvent):
                        log("Proved unsat after generating {} clauses."
                            .format(unprocessed.numGenerated()))
                        return None
        processed.add(next_to_process)
    log("Proved sat after generating {} clauses.".format(unprocessed.numGenerated()))
    return processed

def full_resolution(sent):
    clauses = sent.clauses
    processed = set([])
    unprocessed = clauses
    return general_resolution_solver(processed, unprocessed, lambda x: True)

def unit_resolution(unit_clause, sent):
    clauses = sent.clauses
    processed = set(clauses)
    unprocessed = [unit_clause]
    result = general_resolution_solver(processed, unprocessed, lambda x: len(x) == 1)
    if result is not None:
        return Cnf(result)
    else:
        return None
