import unittest
import cnf
from cnf import check_term


class TestLogicalInference(unittest.TestCase):
    
    def test_literal(self):
        assert cnf.l('!a') == cnf.l('!a')
        assert cnf.l('a') == cnf.l('a')
        assert cnf.l('!a') != cnf.l('!b')
        assert cnf.l('!a') != cnf.l('a')
        assert cnf.l('a') != cnf.l('b')
        assert len(set([cnf.l('!a'), cnf.l('!a'), cnf.l('b'), cnf.l('!c'), cnf.l('b')])) == 3


    def test_clause(self):
        assert cnf.c('d || !c') == cnf.c('!c || d')
        c1 = cnf.c('!a || b || e')
        assert c1['b'] == False
        assert c1['a'] == True
        assert bool(cnf.c('a'))
        assert not bool(cnf.c('FALSE'))
        assert c1.symbols() == {'a', 'b', 'e'}
        assert cnf.c('a || b || e') < cnf.c('b || c || e')
        c2 = c1.remove('a')
        assert c2 == cnf.c('b || e')
        c3 = c1.remove('b')
        assert c3 == cnf.c('!a || e')
        c4 = c1.remove('d')
        assert c4 == c1
        size = len(set([cnf.c('d || !c'), 
                        cnf.c('!c || d'), 
                        cnf.c('b'), 
                        cnf.c('!c || d || !e'), 
                        cnf.c('d || !e || !c')]))
        assert size == 3
        assert str(cnf.c('!c || d')) == '!c || d'
        assert str(cnf.c('FALSE')) == 'FALSE'
        assert cnf.c('!a || !b') | cnf.c('c || d || e') == cnf.c('!a || !b || c || d || e')
        assert cnf.c('!a || c') | cnf.c('c || d || e') == cnf.c('!a || c || d || e')
        assert cnf.c('!a || !c') | cnf.c('c || d || e') is None
        assert 'a' in cnf.c('!a || !c')
        assert 'b' not in cnf.c('!a || !c')
        assert 'c' in cnf.c('!a || !c')
       
    
    def test_model_checker(self):
        sent = cnf.sentence(['!a || b || e', 
                             'a || !b', 
                             'b || !e', 
                             'd || !e', 
                             '!b || !c || !f', 
                             'a || !e', 
                             '!b || f', 
                             '!b || c'])
        model = {'a': -1, 'e': -1, 'b': -1, 'f': 1, 'd': 1, 'c': 1}
        assert check_term(model, sent)
        model = {'a': -1, 'e': -1, 'b': 1, 'f': -1, 'd': -1, 'c': -1}
        assert not check_term(model, sent) 

        
    def test_cnf(self):
        assert cnf.c('d || !c') == cnf.c('!c || d')
        
