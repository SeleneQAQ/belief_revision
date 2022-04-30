import math
import logging
from operator import neg

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Implies, disjuncts
from sortedcontainers import SortedList
from Belief import Belief
import calculations


class BeliefBase:
    def __init__(self):
        self.beliefsSetOriginal = []
        self.beliefsSetCNF = []

    def addBelief(self, belief):
        if self.deleteSameBelief(belief) == 1:
            x = Belief(belief)
            self.beliefsSetOriginal.append(x)
            self.calcutatePlausibilityOrders(self.beliefsSetOriginal)

    def addBlindly(self, belief):
        x = Belief(belief)
        self.beliefsSetOriginal.append(x)
        self.calcutatePlausibilityOrders(self.beliefsSetOriginal)

    def convertToCNF(self):
        self.beliefsSetCNF = []
        for belief in self.beliefsSetOriginal:
            cnfBelief = to_cnf(belief.belief)
            separatedBeliefs = calculations.splitFormula('&', cnfBelief)
            for b in separatedBeliefs:
                x = Belief(b)
                x.plausibilityOrder = belief.plausibilityOrder
                self.beliefsSetCNF.append(x)

    def printCNF(self):
        print('PRINTING CNF: ')
        for belief in self.beliefsSetCNF:
            print(belief.belief, belief.plausibilityOrder)

    def calcutatePlausibilityOrders(self, beliefsSet):
        if len(beliefsSet) == 1:
            pass
        else:
            ratio = 1 / len(beliefsSet)
            i = 0
            for i in range(0, len(beliefsSet)):
                beliefsSet[i].plausibilityOrder = round((i + 1) * ratio, 2)

    # when a new belief come, check if it has same in the original part
    def deleteSameBelief(self, newBelief):

        for belief in self.beliefsSetOriginal:
            if to_cnf(belief.belief) == to_cnf(newBelief):
                self.beliefsSetOriginal.remove(belief)
                self.addBelief(newBelief)
                return 0
        return 1

    def convertToCNFForContraction(self, ConTractionSet):
        SetCNF = []
        for belief in ConTractionSet:
            cnfBelief = to_cnf(belief.belief)
            separatedBeliefs = calculations.splitFormula('&', cnfBelief)
            for b in separatedBeliefs:
                x = Belief(b)
                x.plausibilityOrder = belief.plausibilityOrder
                SetCNF.append(x)
        return SetCNF

    def contraction(self, belief):
        original = self.beliefsSetOriginal
        # sort the belief by the plausibilityOrder
        original.sort(key=lambda x: x.plausibilityOrder, reverse=True)
        # get the contrary of input belief
        contrary_belief = belief
        # transfrom it into CNF
        contrary_beliefCNF = Belief(to_cnf(contrary_belief))
        # the result of contractionSet
        finalSet = []
        contractionSet = []
        contractionSet.append(contrary_beliefCNF)
        # for each element in beliefset, check if it is conflict with contrary of input belief, then we add more element
        # if conflict, we will not input it into the result
        for i in original:
            cnf_i = to_cnf(i.belief)
            contractionSet.append(cnf_i)
            self.calcutatePlausibilityOrders(contractionSet)
            resolution = calculations.unitResolution(self.convertToCNFForContraction(contractionSet), belief)
            if resolution == True:
                print('true res')
                finalSet.append(i)
            if resolution == False:
                contractionSet.remove(cnf_i)
        print('result:')
        print(finalSet)

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
