import json
from sympy import limit, symbols, diff, simplify, S
from sympy.parsing.latex import parse_latex

from format_expressions import format_dict
from negative_roots_handler import subsitute_roots
from e_handler import subs_e

x = symbols("x")

def calculate_derivative(request_dict) -> tuple:
    print(request_dict)
    latex_function = request_dict.get("function") # incoming string will be escaped ex: "\\cos{x}"
    x_0 = str(request_dict.get("x_0")) # because json.loads treats a numeric value inside quotation marks as int

    function = parse_latex(latex_function)
    function = subs_e(function)

    x_0 = parse_latex(x_0)
    x_0 = subs_e(x_0)
    x_0 = subsitute_roots(x_0)

    prime_derivative = diff(simplify(function))

    right_limit = limit(prime_derivative, x, x_0, "+")
    right_limit = subsitute_roots(right_limit)

    left_limit = limit(prime_derivative, x, x_0, "-")
    left_limit = subsitute_roots(left_limit)

    return function, x_0, prime_derivative, right_limit, left_limit

def check_points(function, prime_derivative, right_limit, left_limit, x_0) -> tuple:
    y_0 = subsitute_roots(function.subs(x, x_0))

    # check if they are both finite
    if(not (right_limit == S.Infinity or right_limit == S.NegativeInfinity and left_limit == S.Infinity or left_limit == S.NegativeInfinity)):
        if(right_limit == left_limit):
            if(prime_derivative.subs(x, x_0) == 0): #test this expression
                kind = "stationary_point"
                return y_0, kind
            else:
                kind = "derivable_point"
                return y_0, kind
        else:
            kind = "corner_point"
            return y_0, kind
    
    # check if one is finite and the other is infinite or viceversa
    elif((right_limit == S.Infinity or right_limit == S.NegativeInfinity) and not(left_limit == S.Infinity or left_limit == S.NegativeInfinity) or (left_limit == S.Infinity or left_limit == S.NegativeInfinity) and not(right_limit == S.Infinity or right_limit == S.NegativeInfinity)):
        kind = "corner_point"
        return y_0, kind
    
    # check if they are both infinite
    else:
        if(right_limit == left_limit):
            kind = "vertical_tangent"
            return y_0, kind
        else:
            kind = "cusp"
            return y_0, kind
        

def calculate_point_of_differentiability(request_dict):
    function, x_0, prime_derivative, right_limit, left_limit = calculate_derivative(request_dict)
    y_0, kind = check_points(function, prime_derivative, right_limit, left_limit, x_0)

    response_dict = {
        "function": function, 
        "derivative": prime_derivative,
        "points": [
            {
                "x_0": x_0,
                "y_0": y_0,
                "kind": kind
                },
        ]
    }
    return json.dumps(format_dict(response_dict))

