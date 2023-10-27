from sympy import symbols, E

def subs_e(expression):
    e = symbols("e")
    new_expression = expression.subs(e, E)
    return new_expression