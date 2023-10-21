from sympy import Mul ,Integer, Pow, Rational, real_root, oo, preorder_traversal

def get_root_args(root) -> tuple:
    return root.args

def is_negative_root(root: tuple) -> bool:
    # 1. the base has to be negative
    # 2. the exponent of the pow needs to be a fraction
    # 3. the denominator of the exponent needs to be odd
    base, exp = root
    if(not base.is_negative):
        return False
    if(exp.is_integer and not exp.is_rational):
        return False
    if(not exp.q % 2 == 1):
        return False
    
    return True

def get_real_solution(root: tuple):
    if(is_negative_root(root)):
        base, exp = root
        arg = base
        radical_number = exp.q

        return real_root(arg, radical_number)
    
def subsitute_roots(expr):
    new_expr = expr
    for arg in preorder_traversal(expr):
        if(type(arg) == Pow):
            real_solution = get_real_solution(get_root_args(arg))
            new_expr = new_expr.subs(arg, real_solution)
    return(new_expr)