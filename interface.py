import argparse
import logging

from sympy import to_cnf, SympifyError

from BeliefBase import BeliefBase


##
# variables a user can use as for now: p and q 
##
logic = ['p','q']

allBeliefs = BeliefBase()


def menu():
    print("press button to do action: ")
    print('m: menu')
    print('a: add belief')
    print('p: print all beliefs')


def checkPossibilityOrder():
    # prin()
    logical_things = []
    belief_possibility = {}

    for i in range(2**len(logic)):
        line = ''
        for j in range(len(logic)):
            if i//2**j%2 == 0:
                line += logic[j].lower()
            else:
                line += logic[j].upper()
        logical_things.append(line)
        belief_possibility[line] = []

        print(f'\t{line}', end='')
    print()
    print()
    # print(logical_things)

    
    for bs in allBeliefs.beliefsSet:
        print(f'{bs.belief}\t' , end='')
        for log in logical_things:
            # print(f'{log}\t', end='')
            val = 0
            for l in log:
                if l in str(bs.belief):
                    val = 1
            
            belief_possibility[log].append(val)
            print(f'{val}\t', end='')

        # belief_possibility[bs.belief] = pos_list.copy()
        print()
    
    for th in logical_things:
        pos = sum(belief_possibility[th])/len(belief_possibility[th])
        print(f'\t%.2f' % pos, end='')


    # print(allBeliefs.beliefsSet)





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

