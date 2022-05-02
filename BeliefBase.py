import math
import logging
from operator import neg

from sympy.logic.boolalg import to_cnf, And, Or, Equivalent, Implies, disjuncts
from Belief import Belief
import calculations


class BeliefBase:
    def __init__(self):
        self.beliefsSetOriginal = []
        self.beliefsSetCNF = []

    def __eq__(self, other):
        return self.beliefsSetOriginal == other.beliefsSetOriginal

    def addBelief(self, belief):
        if self.deleteSameBelief(belief) == 1:
            
            x = Belief(belief)
            self.beliefsSetOriginal.append(x)
            self.calcutatePlausibilityOrders(self.beliefsSetOriginal)

    def addBliefWithOrder(self, belief, plausibilityOrder):
        x = Belief(belief)
        x.plausibilityOrder = plausibilityOrder
        self.beliefsSetOriginal.append(x)

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
                #print('Previous belief: ', belief.belief, 'order:', belief.plausibilityOrder, 'is the same.')
                #print('Deleting it before adding new belief', newBelief, 'with order 1' )
                self.beliefsSetOriginal.remove(belief)
                self.addBelief(newBelief)
                return 0
        return 1

    def AGMContractionSuccess(self, newBelief):
        for belief in self.beliefsSetOriginal:
            if to_cnf(belief.belief) == to_cnf(newBelief):
                return 0
        return 1

    def AGMContractionInclusion(self, oriBeliefSet):
        counter = 0
        for belief in self.beliefsSetOriginal:
            for oribelief in oriBeliefSet.beliefsSetOriginal:
                if belief.belief == oribelief.belief:
                    counter += 1
        if counter == len(self.beliefsSetOriginal):
            return 1
        return 0


    def __repr__(self):
        if len(self.beliefsSetOriginal) == 0:
            return 'empty'
        return '\n'.join(str(x) for x in self.beliefsSetOriginal)
