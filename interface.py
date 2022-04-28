import argparse
import logging

from sympy import to_cnf, SympifyError

from BeliefBase import BeliefBase
import Belief
import calculations


##
# variables a user can use as for now: p and q 
##
logic = ['p','q']

# allBeliefs = BeliefBase()


def menu():
    print("Press button to do action: ")
    print('m: Menu')
    print('a: Add belief')
    print('c: Calculate possibility order')
    print('p: Print all beliefs')
    print('r: Resolution')
    print('q: Quit')



def checkPossibilityOrder(allBeliefs):
    print()
    logical_things = []
    belief_possibility = {}

    for i in range(2**len(logic)):
        line = ''
        for j in range(len(logic)):
            if i//2**j%2 == 0:
                line += ' ' + logic[j].lower()
            else:
                line += ' ~' + logic[j].lower()
                # line += logic[j].upper()

        logical_things.append(line)
        belief_possibility[line] = []

        print(f'\t{line}', end='')
    print()
    print()
    # print(logical_things)

    
    for i in range(len(allBeliefs.beliefsSetOriginal)):
        print(f'{allBeliefs.beliefsSetOriginal[i].belief}\t' , end='')
        for log in logical_things:
            # print(f'{log}\t', end='')
            val = 0
            
            # for l in log:
            j = 0
            sentance = str(allBeliefs.beliefsSetCNF[i].belief)
            while j < len(sentance):
            # for j in range(len(log)):
                # print(f'j = {j}')
                
                if sentance[j] == ' ':
                    j += 1
                    continue
                testString = sentance[j]
                if sentance[j] == '~':
                    testString += sentance[j+1]
                    j += 1

                # print(f'Athuga hvort {testString} sé í {log}' )
                if testString in log.split(' '):
                    val = 1
                
                j += 1
            
            belief_possibility[log].append(val)

            print(f'{val}\t', end='')

        # belief_possibility[allBeliefs.beliefsSetOriginal[i].belief] = pos_list.copy()
        print()
    
    for th in logical_things:
        pos = sum(belief_possibility[th])/len(belief_possibility[th])
        print(f'\t%.2f' % pos, end='')

    print()


    # print(allBeliefs.beliefsSet)





def interfaceLoop(allBeliefs):
    
    action = input()
    if action =='m':
        menu()

    elif action == 'a':
        print('Enter belief: ')
        belief = input()
        allBeliefs.addBelief(belief)

    elif action == 'c':
        checkPossibilityOrder(allBeliefs)

    elif action == 'p':
        print('Size of beleife base: ', len(allBeliefs.beliefsSetOriginal))
        print('Printing Belief Base: ')
       
        print(allBeliefs)
       

    elif action == 'q':
        return

    elif action == 'r':
        print('Enter belief: ')
        belief = input()
        
        calculations.unitResolution(allBeliefs.beliefsSetOriginal, Belief(belief))

    else:
        print('wrong input. press button to do action: ')
        interfaceLoop(allBeliefs)

    print("DONE. press button to do action: ")
    interfaceLoop(allBeliefs)
    

if __name__ == '__main__':
    allBeliefs = BeliefBase()
    allBeliefs.addBelief('((p|q)>>r)&(r>>(p|q))')
    menu()
    interfaceLoop(allBeliefs)

