def rule_AND(a, b):
    if a == 1 and b == 1:
        return 1
    else:
        return 0


def rule_OR(a, b):
    if a == 0 and b == 0:
        return 0
    else:
        return 1


def rule_NOT(a):
    if a == 0:
        return 1
    if a == 1:
        return 0


def rule_IF(a, b):
    if a == 1 and b == 0:
        return 0
    else:
        return 1


def rule_BI_IF(a, b):
    if a == 1 and b == 1:
        return 1
    elif a == 0 and b == 0:
        return 1
    else:
        return 0


print(rule_BI_IF(1, 1))
