
import math
import logging
from operator import neg

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Implies
from sortedcontainers import SortedList
from Belief import Belief

class BeliefBase:
    def __init__(self):
        self.beliefsSet = []

    def addBelief(self, belief, plausibilityOrder):
        if self.deleteSameBelief(belief, plausibilityOrder) == 1:
            x = Belief(belief, plausibilityOrder)
            self.beliefsSet.append(x)

    def deleteSameBelief(self, newBelief, plausibilityOrder):
        for belief in self.beliefsSet:
            if to_cnf(belief.belief) == to_cnf(newBelief):
                belief.belief = newBelief
                belief.plausibilityOrder = plausibilityOrder
                return 0
        return 1



    def resolution(self, belief, plausibilityOrder):
        formula = to_cnf('~('+belief+')')
        print(formula)


    def __repr__(self):
        if len(self.beliefsSet) == 0:
            return 'empty'
        return '\n'.join(str(x) for x in self.beliefsSet)



