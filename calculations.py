from sympy.logic.boolalg import to_cnf
import BeliefBase
import Belief

def unitResolution(beliefBase, newBelief): #input only belief orginal array
    #newBeliefBase = beliefBase + newBelief
    #Get all the pairs to find the resolvant
    allPairs = []
    clausesAfterResolution = set()
    isResolutionFinished = False
 
    #print('beliefBase', beliefBase, 'newBelief: ', to_cnf(newBelief))
    if len(beliefBase) == 1: #len(to_cnf(newBelief)):
        return False
    while isResolutionFinished ==False:
        sizeOfBeliefBase = len(beliefBase)
        allPairs = [(beliefBase[i], beliefBase[j])
                 for i in range(sizeOfBeliefBase) for j in range(i + 1, sizeOfBeliefBase)]

        #print('pairs: ', allPairs)

        for [clause1, clause2] in allPairs:
            clause1 = to_cnf(clause1.belief)
            clause2 = to_cnf(clause2.belief)
            #print('clause 1: ', clause1, ' clause 2: ', clause2)
            resolvant = factor_clauses(clause1, clause2)
            #print('new clause from resolvant: ', resolvant)
            if False in resolvant:
                #print('resolution finished, sucess')
                return True
                #continue

            beliefs = []
            for belief in beliefBase:
                beliefs.append(belief.belief)

            
            clausesAfterResolution = set(clausesAfterResolution.union(set(resolvant)))
        #print('clauses: ', clausesAfterResolution, 'beliefset: ', set(beliefs))
    #if len(clausesAfterResolution) >0:
        if clausesAfterResolution.issubset(set(beliefs)):
            isResolutionFinished = True
            #print('resolution finished, failed')
            return False

        new = Belief.Belief('hehh')
        for iteral in clausesAfterResolution:
            ifCanAdd = True
            #print('comparing  this:')
            #print(iteral, type(iteral))
            #print('with this: ')
            for existingIterals in beliefBase:
                
                #print(existingIterals.belief,  type(existingIterals.belief))
                if iteral == str(existingIterals.belief):    
                    ifCanAdd = False
                    break
                    
            if ifCanAdd ==True:
                new = Belief.Belief(iteral) 
                #print('appended: ', iteral)
                beliefBase.append(new)
            #print(beliefBase)

        #if len(clausesAfterResolution) == 0:
        #    print('resolution finished, failed clauses were empty')
        #    return False
                        
               
def factor_clauses(clause1, clause2):
    #print()
    literals1 = str(clause1).replace(" ", "").split('|')
    literals2 = str(clause2).replace(" ", "").split('|')

    new_clause = []
    #print('entered resolvant with: ',clause1, ' ',  clause2)
    for l1 in literals1:
        for l2 in literals2:
            #print(l1, ' ',  l2)
            if f'{l1}' == f'~{l2}' or f'~{l1}' == f'{l2}':
                a = literals1.copy()
                a.remove(l1)
                b = literals2.copy()
                b.remove(l2)     
                #print(a, '+', b)
                # Use set to remove dublicates
                clause = list(set(a + b))
                if clause == []:
                    
                    new_clause.append(False)
                else:
                    # print('clause:', clause)
                    clause_text = '|'.join(clause)
                    new_clause.append('|'.join(clause))
                #print('enetered the equality',a,  b,  clause  )
                    # print('clause text:', clause_text)
    #print('returned clause: ', new_clause)     
    return new_clause

def validityCheck(newBelief, allowedSigns):
    q = ""
    for i in newBelief:
        #print(i)
        if i.isalpha():
            q = "".join([q,i])
    #print('result', q)
    for i in q:
        if i not in allowedSigns:
            print('not allowed logic signs deteced. please use only: ', allowedSigns)
            return False
        #uniqueSign = True
        #for x in BeliefBase:
        #    if i in x:
        #        uniqueSign = False
        #        break
        #if uniqueSign == True:
        #    print(i, ' is new in database, add it ')
        #    return True
    return True

    



def splitFormula(splitSign, formula):
    # formula - one clause in cnf 
    if splitSign == '&':
        return dissociate(splitSign, formula)
    else: print('splitFormula in calculations error. Split sign not implemented')

def dissociate(op, args):
    # function from https://github.com/aimacode/aima-python/blob/master/logic.py
    """Given an associative op, return a flattened list result such
    that Expr(op, *result) means the same as Expr(op, *args).
    >>> dissociate('&', [A & B])
    [A, B]
    """
    result = []
    args = to_cnf(args)
    operations =[ '|','(', ')']
    def collect(subargs):
        subargs = str(subargs)
        #print(subargs)

        for i in range(0, len(str(subargs))):
            #print(subargs[i])
            if subargs[i] == op:      
                result.append(' ')
                #print(subargs[i+1: len(str(subargs))-1])
                #collect(subargs[i+1: len(str(subargs))-1])
            elif subargs[i] == ' ':
                continue
            elif subargs[i] in  operations:
                if result == []:
                    #print('empty')
                    result.append(subargs[i])
                else:     
                    result[-1] = result[-1] + subargs[i] 
                #print('adding to result: ', result[-1], subargs[i])
            else:
                if result == []:
                    result.append(subargs[i])
                else: result[-1] = result[-1] + subargs[i]
            #    print('current result:',  result[-1])
            #print('end of for loop', result)

    collect(args)
    return result
