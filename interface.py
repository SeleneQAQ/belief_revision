import argparse
import logging

from sympy import to_cnf, SympifyError
from agm_functions import checkConsistency, checkVacuity

from BeliefBase import BeliefBase
import Belief
from calculations import unitResolution, splitFormula, validityCheck
import copy

##
# variables a user can use as for now: p and q 
##
logic = ['p','q', 'r']

# allBeliefs = BeliefBase()

def welcome():
    print('Welcome to belief revision program. You can add new beliefs by revision,')
    print('contraction updates the Belief Base by removing the clauses that implies the input to contract with')

def menu():
    
    print("Press button to do action: ")
    print('m: Menu')
    print('p: Print all beliefs')
    print('r: revision')
    print('c: contraction')

    print('agm: Test for agm postulates')
    print('pos: Calculate possibility order')
    print('res: Resolution')
    print('q: Quit')

def contraction(allBeliefs, belief):
    belief = belief.lower()
    contrary_belief = "~(" + belief + ")"
    contrary_belief = to_cnf(contrary_belief)
    oriBeliefsSet = copy.deepcopy(allBeliefs)
    newBeliefsSet = BeliefBase()
    resultBeliefsSet = BeliefBase()
    allBeliefs.beliefsSetOriginal.sort(key=lambda x: x.plausibilityOrder, reverse=True)
    for i in allBeliefs.beliefsSetOriginal:
        newBeliefsSet.addBlindly(contrary_belief)
        newBeliefsSet.addBlindly(i.belief)
        newBeliefsSet.convertToCNF()
        resolution = unitResolution(newBeliefsSet.beliefsSetCNF, belief)
        if resolution == False:
            resultBeliefsSet.addBliefWithOrder(i.belief, i.plausibilityOrder)
            newBeliefsSet = copy.deepcopy(resultBeliefsSet)
        if resolution == True:
            newBeliefsSet = copy.deepcopy(resultBeliefsSet)
    #print(resultBeliefsSet)
    #print('ContractionSuccess: ', allBeliefs.AGMContractionSuccess(belief))
    #print('InclusionSuccess: ', allBeliefs.AGMInclusionSuccess(oriBeliefsSet))

    resultBeliefsSet.beliefsSetOriginal.sort(key=lambda x: x.plausibilityOrder, reverse=False)
    return resultBeliefsSet

def checkPossibilityOrder(beliefs):
    print()
    logical_things = []
    belief_possibility = {}

    beliefsInCNF = []
    longest_logic = 0
    for i in range(len(beliefs.beliefsSetOriginal)):
        cnfbelief = to_cnf(beliefs.beliefsSetOriginal[i].belief)
        # print(beliefs.beliefsSetOriginal[i].belief, 'to CFN:', cnfbelief)
        beliefsInCNF.append(cnfbelief)

        if len(beliefs.beliefsSetOriginal[i].belief) > longest_logic:
            longest_logic = len(beliefs.beliefsSetOriginal[i].belief)

    # print()
    # print('longest logic:', longest_logic)

    print(''.rjust(longest_logic, " "), end='')
    for i in range(2**len(logic)):
        line = ''
        for j in range(len(logic)):
            if i//2**j%2 == 0:
                line += '  ' + logic[j].lower()
            else:
                line += ' ~' + logic[j].lower()
                # line += logic[j].upper()

        logical_things.append(line)
        belief_possibility[line] = []

        print(line.rjust((3*len(logic))+1, " "), end='')
        
    print()
    print()
    # print(logical_things)

    
    for i in range(len(beliefs.beliefsSetOriginal)):
        print(beliefs.beliefsSetOriginal[i].belief.ljust(longest_logic, " ") , end='')
        for log in logical_things:

            # print(f'{log}\t', end='')
            # for l in log:
            sentences = str(beliefsInCNF[i]).split('&')
            total = 0
            for sentence in sentences:
                
                j = 0
                while j < len(sentence):
                # for j in range(len(log)):
                    # print(f'j = {j}')
                    
                    if sentence[j] == ' ':
                        j += 1
                        continue
                    testString = sentence[j]
                    if sentence[j] == '~':
                        testString += sentence[j+1]
                        j += 1
                    
                    # print(f'Athuga hvort {testString} sé í {log}')

                    if testString in log.split(' '):
                        total += 1
                        break # If one element is true in list of or's the whole list is true

                    j += 1

            if total == len(sentences):
                val = 1
            else:
                val = 0
            
            belief_possibility[log].append(val)

            print(str(val).center((3*len(logic))+1, " "), end='')
   

        # belief_possibility[allBeliefs.beliefsSetOriginal[i].belief] = pos_list.copy()
        print()
    
    print(''.rjust(longest_logic, " "), end='')
    for th in logical_things:
        pos = sum(belief_possibility[th])/len(belief_possibility[th])
        print(('%.2f' % pos).center((3*len(logic))+1, " "), end='')

    print()


    # print(allBeliefs.beliefsSet)


def interfaceLoop(allBeliefs):
    
    action = input()
    action = action.lower()
    if action =='m':
        menu()

    elif action == 'pos':
        checkPossibilityOrder(allBeliefs)

    elif action == 'c':
        
        print('Enter belief that you do not want to believe in now: ')
        belief = input()
        isInputValid = validityCheck(belief, logic)
        if isInputValid == False: interfaceLoop(allBeliefs)

        allBeliefs= copy.deepcopy(contraction(allBeliefs, belief))

    elif action == 'p':
        print('Size of belief base: ', len(allBeliefs.beliefsSetOriginal))
        print('Printing Belief Base: ')
       
        print(allBeliefs)
       

    elif action == 'q':
        return

    elif action == 'agm':
        print('Enter belief: ')
        belief = input()
        belief = belief.lower()

        isInputValid = validityCheck(belief, logic)
        if isInputValid == False: interfaceLoop(allBeliefs)

        contrary_belief = "~(" + belief + ")"

        set1 = copy.deepcopy(allBeliefs)
        set2 = copy.deepcopy(allBeliefs)### have to use multiple copies since some reorderign is done with deepcopy that conflicts with equaltiy
        set3 = copy.deepcopy(allBeliefs)### have to use multiple copies since some reorderign is done with deepcopy that conflicts with equaltiy

        ### vacuity
        vacuity = checkVacuity(set2, belief)
        print(vacuity)
        print("")
        print("")

        ### consitency
        print("consistency check:")
        bbConsistency = checkConsistency(set1, "belief base")
        print("belief base is consistent:", bbConsistency)
        print("")

        disallowed_characters = "()"
        form = belief.split("&")

        for i in range(len(form)):
            for character in disallowed_characters:
                form[i] = form[i].replace(character, "")
        bs = BeliefBase()

        for bel in form:
            bs.addBlindly(bel)

        phiConsistency = checkConsistency(bs, "phi")
        print("phi is consistent:", phiConsistency)
        print("")

        ## revision
        set3 = copy.deepcopy(contraction(set3, contrary_belief))
        set3.addBelief(belief)

        revisedConsistency = checkConsistency(set3, "revised set")
        print("revised set is consistent:", revisedConsistency)
        print("")

        if bbConsistency:
            if phiConsistency:
                if revisedConsistency:
                    print("B is consistent, phi is consistent, B*phi is consistent")
                    print("consistency holds")
                else:
                    print("B is consistent, phi is consistent, B*phi is inconsistent")
                    print("consistency doesnt hold")
            else:
                print("B is consistent, phi is inconsistent")
                print("phi needs to be consistent to check for consistency postulate")
        else:
            print("inconsistency in belief base")


    elif action == 'r':
        print('Enter belief: ')
        belief = input()
        belief = belief.lower()

        contrary_belief = "~(" + belief + ")"

        isInputValid = validityCheck(belief, logic)
        if isInputValid == False: interfaceLoop(allBeliefs)

        allBeliefs = copy.deepcopy(contraction(allBeliefs, contrary_belief))
        allBeliefs.addBelief(belief)

    elif action == 'res':
        print('Entered resolution. It will do the resolution with the Belief base and the input you enter. ')
        print('Enter belief: ')
        belief = input()
        belief = belief.lower()
        
        #contrary_belief = "~("+belief+")"
        contrary_belief = belief
        contrary_belief = to_cnf(contrary_belief)
        split_contrary_belief = splitFormula('&', contrary_belief)
       
        newBeliefsSet = copy.deepcopy(allBeliefs)
        newBeliefsSet.addBlindly(contrary_belief)
        newBeliefsSet.convertToCNF()
        newBeliefsSet.printCNF()
        #newBelief = newBeliefsSet.beliefsSet[-1] # get last element, so the belief just enetered by user
        isInputValid = validityCheck(belief, logic)
        if isInputValid == False: interfaceLoop(allBeliefs)

        resolution = unitResolution(newBeliefsSet.beliefsSetCNF, belief)
        if resolution == False:
            allBeliefs.addBelief(belief)

    else:
        print('wrong input. press button to do action: ')
        interfaceLoop(allBeliefs)
    print()
    print("DONE. press button to do action: ")
    interfaceLoop(allBeliefs)
    

if __name__ == '__main__':
    welcome()
    allBeliefs = BeliefBase()
    allBeliefs.addBelief('p|q')
    allBeliefs.addBelief('p>>q')
    allBeliefs.addBelief('p&q')
    menu()
    interfaceLoop(allBeliefs)
