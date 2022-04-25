
import math
import logging
from operator import neg

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent
from sortedcontainers import SortedList
from Belief import Belief

class BeliefBase:
    def __init__(self):
        self.beliefsSet = [] 

    def addBelief(self, belief, plausibilityOrder):
        formula = to_cnf(belief)
        x = Belief(formula, plausibilityOrder)
        self.beliefsSet.append(x)

    def __repr__(self):
        if len(self.beliefsSet) == 0:
            return 'empty'
        return '\n'.join(str(x) for x in self.beliefsSet)



