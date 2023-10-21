from sympy.printing.latex import latex
import re

## define a function that takes a dict and does format operation for each value then returns new dict
def format_dict(dict):
    derivative = dict.get("derivative")
    function = dict.get("function")
    points = dict.get("points")

    derivative = latex(derivative, ln_notation=True)
    function = latex(function, ln_notation=True)

    # \right) and \left( are not supported by katex, renderer used in frontend
    derivative = re.sub(r"\\right", "", derivative)
    dict["derivative"] = re.sub(r"\\left", "", derivative)

    function = re.sub(r"\\right", "", function)
    dict["function"] = re.sub(r"\\left", "", function)

    for i in range(len(points)):
        x_0 = points[i].get("x_0")
        y_0 = points[i].get("y_0")

        x_0 = latex(x_0, ln_notation=True)
        y_0 = latex(y_0, ln_notation=True)
        
        x_0 = re.sub(r"\\right", "", x_0)
        dict["points"][i]["x_0"] = re.sub(r"\\left", "", x_0)

        y_0 = re.sub(r"\\right", "", y_0)
        dict["points"][i]["y_0"] = re.sub(r"\\left", "", y_0)

    return dict
