import argparse
import logging

from sympy import to_cnf, SympifyError

from BeliefBase import BeliefBase


def menu():
    print("press button to do action: ")
    print('m: menu')
    print('a: add belief')
    print('p: print all beliefs')


def interfaceLoop(allBeliefs):
    
    action = input()
    if action =='m':
        menu()

    elif action == 'a':
        print('Enter belief: ')
        belief = input()
        print('Enter plausibility order')
        plausibilityOrder = input()
        allBeliefs.addBelief(belief, plausibilityOrder)


    elif action == 'p':
        print('Printing Belief Base: ')
        print(allBeliefs)
        
    else:
        print('wrong input. press button to do action: ')
        interfaceLoop(allBeliefs)

    print("DONE. press button to do action: ")
    interfaceLoop(allBeliefs)
    

if __name__ == '__main__':
    allBeliefs = BeliefBase()

    menu()
    interfaceLoop(allBeliefs)

