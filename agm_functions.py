import copy
from sympy import to_cnf, SympifyError
from BeliefBase import BeliefBase
from calculations import unitResolution, splitFormula, validityCheck


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

def checkVacuity(beliefSet, phi):
    bs = copy.deepcopy(beliefSet)
    old_bs = copy.deepcopy(beliefSet)
    bs.addBlindly(phi)
    bs.convertToCNF()

    contrary_belief = "~(" + phi + ")"

    vac_resolution = unitResolution(bs.beliefsSetCNF, contrary_belief)

    revised_set = copy.deepcopy(contraction(beliefSet, contrary_belief))
    revised_set.addBelief(phi)

    ### vacuity
    print("vacuity check:")
    print("if ~p is not a memeber of b, b*p = b+p:")
    if vac_resolution:
        print(contrary_belief, "is not a member of belief set, vacuity holds")
        vacuity = True
    else:
        old_bs.addBelief(phi)
        print("b+p", old_bs.beliefsSetOriginal)
        print("b*p", revised_set.beliefsSetOriginal)
        vacuity = (old_bs == revised_set)
        print("if sets are similar vacuitity holds:", vacuity)
    return vacuity

def checkConsistency(beliefSet, name):
    bs = copy.deepcopy(beliefSet)
    beliefs = bs.beliefsSetOriginal
    print("testing " + name + " consistency with beliefs:")
    print(bs.beliefsSetOriginal)
    print("")
    for bel in beliefs:
        bel = bel.belief
        notBel = "~(" + bel + ")"
        print("Contracting with:", notBel)
        contracted_bs = contraction(bs, notBel)
        bs = copy.deepcopy(beliefSet)
        bs_consistency = (contracted_bs == bs)

        if bs_consistency:
            print("success, "+ name + " does not imply:", notBel)
        else:
            print(name + " is inconsistent; implies:", notBel)
            break

    return bs_consistency

    def checkSuccess(revisionBeliefSet, belief):
        bs = copy.deepcopy(revisionbeliefSet)
        beliefs = bs.beliefsSetOriginal
        print(belief)
        for bel in beliefs:
            bel = bel.belief
            print(bel)

            success = (bel == belief)
            if success:
                break

        return success