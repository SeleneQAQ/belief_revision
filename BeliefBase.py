import math
import logging
from operator import neg

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Implies, disjuncts
from sortedcontainers import SortedList
from Belief import Belief


class BeliefBase:
    def __init__(self):
        self.beliefsSetOriginal = []
        self.beliefsSetCNF = []

    def addBelief(self, belief):
        if self.deleteSameBelief(belief) == 1:
            x = Belief(belief)
            self.beliefsSetOriginal.append(x)
            self.calcutatePlausibilityOrders(self.beliefsSetOriginal)

    def calcutatePlausibilityOrders(self, beliefsSet):
        if len(beliefsSet) == 1:
            pass
        else:
            ratio = 1/len(beliefsSet)
            i = 0
            for i in range(0, len(beliefsSet)):
                beliefsSet[i].plausibilityOrder = (i+1)*ratio

            

    #when a new belief come, check if it has same in the original part
    def deleteSameBelief(self, newBelief):
        
        for belief in self.beliefsSetOriginal:
            if to_cnf(belief.belief) == to_cnf(newBelief):
                #belief.belief = newBelief
                #belief.plausibilityOrder = 1.0
                self.beliefsSetOriginal.remove(belief)
                self.addBelief(newBelief)
                return 0
        
        return 1

    def resolution(self, belief):
        formula = to_cnf(belief)
        anti_formula = to_cnf('~(' + belief + ')')
        print([formula])

        
        if self.deleteSameBelief(belief) == 1:
            x = Belief(belief)
            self.beliefsSetOriginal.append(x)
            self.beliefsSetCNF.append(Belief(formula))
            element = self.divideElement([formula], And)
            self.calcutatePlausibilityOrders(self.beliefsSetOriginal)
            for i in element:
                print(i)


    # divide belief by op
    def divideElement(self, ori, op):
        result = []

        def divide(subargs):
            for arg in subargs:
                if isinstance(arg, op):
                    divide(arg.args)
                else:
                    result.append(arg)

        divide(ori)
        return result

    def __repr__(self):
        if len(self.beliefsSetOriginal) == 0:
            return 'empty'
        return '\n'.join(str(x) for x in self.beliefsSetOriginal)
