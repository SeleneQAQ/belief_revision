# rule of conjunction
def rule_Con(a, b):
    if a == 1 and b == 1:
        return 1
    else:
        return 0


# rule of disjunction
def rule_Dis(a, b):
    if a == 0 and b == 0:
        return 0
    else:
        return 1


# rule of negation
def rule_Neg(a):
    if a == 0:
        return 1
    if a == 1:
        return 0


# rule of implication
def rule_Imp(a, b):
    if a == 1 and b == 0:
        return 0
    else:
        return 1


# rule of biconditional
def rule_Bic(a, b):
    if a == 1 and b == 1:
        return 1
    elif a == 0 and b == 0:
        return 1
    else:
        return 0
