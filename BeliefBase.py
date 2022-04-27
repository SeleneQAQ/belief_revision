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
            ratio = 1 / len(beliefsSet)
            i = 0
            for i in range(0, len(beliefsSet)):
                beliefsSet[i].plausibilityOrder = (i + 1) * ratio

    # when a new belief come, check if it has same in the original part
    def deleteSameBelief(self, newBelief):

        for belief in self.beliefsSetOriginal:
            if to_cnf(belief.belief) == to_cnf(newBelief):
                self.beliefsSetOriginal.remove(belief)
                self.addBelief(newBelief)
                return 0
        return 1

    def resolution(self, belief):
        # transform the input belief into CNF
        formula = to_cnf(belief)
        anti_formula = to_cnf('~(' + belief + ')')
        print(formula)
        # divide the input belief by & - like (p|r)&(q|r) will be divide into [(p|r),(q|r)]
        element = self.divideElement([formula], And)
        # before input, check if there exists same belief in the original belief set
        if self.deleteSameBelief(belief) == 1:
            # divide the input belief by | - like (p|r) will be divide into [p,r]
            element_single_set = []
            for i in element:
                element_single_set.append(self.divideElement([i], Or))
            # divide belief in original belief set by &
            for originalBelief in self.beliefsSetOriginal:
                ori_element = self.divideElement([to_cnf(originalBelief.belief)], And)
                ori_element_set = []
                for j in ori_element:
                    ori_element_set.append(self.divideElement([j], Or))
            # list of input belief
            print(element_single_set)
            # list of original belief
            print(ori_element_set)

            x = Belief(belief)
            self.beliefsSetOriginal.append(x)
            self.beliefsSetCNF.append(Belief(formula))
            self.calcutatePlausibilityOrders(self.beliefsSetOriginal)
        else:
            return

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
