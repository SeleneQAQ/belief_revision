from sympy.logic.boolalg import to_cnf
import BeliefBase

def unitResolution(beliefBase, newBelief): #input only belief orginal array
    #newBeliefBase = beliefBase + newBelief
    #Get all the pairs to find the resolvant
    allPairs = []
    clausesAfterResolution = set()
    isResolutionFinished = False
    while isResolutionFinished ==False:
        sizeOfBeliefBase = len(beliefBase)
        allPairs = [(beliefBase[i], beliefBase[j])
                 for i in range(sizeOfBeliefBase) for j in range(i + 1, sizeOfBeliefBase)]


        #for i in range(0, sizeOfBeliefBase-1):
        #    primaryClause = to_cnf(beliefBase[i].belief) 
        #    print('primary clasue: ', primaryClause)
        #    for j in range(i+1, sizeOfBeliefBase):
        #        nextClause = to_cnf(beliefBase[j].belief)
        #        pair = [(primaryClause, nextClause)]
        #        print('next clause: ', nextClause)
        #        allPairs.append(pair)
        print('pairs: ', allPairs)
        print('size: ', len(allPairs))
        for [clause1, clause2] in allPairs:
            clause1 = to_cnf(clause1.belief)
            clause2 = to_cnf(clause2.belief)
            print('clause 1: ', clause1, ' clause 2: ', clause2)
            resolvant = factor_clauses(clause1, clause2)
            print('new clause from resolvant: ', resolvant)
            if resolvant == []:
                print('resolution finished, sucess')
                return True
            clausesAfterResolution.union(set(resolvant))
            
        if clausesAfterResolution.issubset(set(beliefBase)):
            isResolutionFinished = True
            print('resolution finished, failed')
            return False
           
        else:
            for iteral in clausesAfterResolution:
                if iteral not in beliefBase.belief:
                    beliefBase.append(iteral)


def factor_clauses(clause1, clause2):

    literals1 = str(clause1).replace(" ", "").split('|')
    literals2 = str(clause2).replace(" ", "").split('|')

    new_clause = []

    for l1 in literals1:
        for l2 in literals2:
            print('What we have here is:', l1, l2)
            if l1 == f'~{l2}' or f'~{l1}' == l2:
                print()
                print('l1:', l1, 'l2:', l2)

                a = literals1.copy()
                a.remove(l1)
                b = literals2.copy()
                b.remove(l2)

                # Use set to remove dublicates
                clause = list(set(a + b))
                # print('clause:', clause)
                clause_text = '|'.join(clause)
                new_clause.append('|'.join(clause))
                # print('clause text:', clause_text)
                
    return new_clause