import expressions
from forwardmode import forwardmodevisitor
from traversal import evalpostvisitor, adjointprevisitor, symbolnodes, adjoint
import numpy as np
import time


def reversemodeAD(expr, conditions):
    """Return dict of the derivatives of expr w.r.t symbols"""
    symbols = dict()
    try:
        evalpostvisitor(expr, symbol_map=conditions)  # Forward traverse
    except ZeroDivisionError:  # Not currently used i dont think
        raise Exception("Function not valid at initial condition")

    if isinstance(expr, np.ndarray):
        for symbol in conditions.keys():
            symbols[symbol] = []
        for expression in expr:
            symbol.adjoint = 0
            adjointprevisitor(expression)  # Backwards traverse through the tree
            for symbol in conditions.keys():
                symbols[symbol].append(symbol.adjoint)  # Store the adjoint values
                symbol.adjoint = 0  # So that next pass the adjoint symbols are set back to 0
    else:
        adjointprevisitor(expr)  # Backwards traverse through the tree
        # For each symbol, return the dict of the repsective adjoint
        for symbol in conditions.keys():
            symbols[symbol] = symbol.adjoint
    return symbols

# Below is just code to run examples and test runtime

#So random arrays are same each time
np.random.seed(0)
# Set how many x,y values we want
n = 10
# Array of initial conditions
w = [np.random.randn(1, 100000) for i in range(n)]

# Array of x symbols
x = [expressions.Symbol(f'x{i}') for i in range(n)]
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()
conditions = dict(zip(x, w)) # Note our symbol map, maps the specific x symbol exprs to the value not 'x' value/str

# Mess around with this to see what happens, write any expr and I.V.
expression = np.asarray([log(x[0]**2)*x[9] + 2*x[1]*x[2]*cos(x[3]**4), exp(x[5]**2)*sin(x[8]*x[6]**2)+x[6]*x[8]])

start = time.time()
reverse = reversemodeAD(expression, conditions)
end = time.time()
print(f"Time for RM AD:{end-start}")

# Redefining prev expr so we adjoint = 0
x = [expressions.Symbol(f'x{i}') for i in range(n)]
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()
conditions = dict(zip(x, w))
# New expression with our new symbols
expression = np.asarray([log(x[0]**2)*x[9] + 2*x[1]*x[2]*cos(x[3]**4), exp(x[5]**2)*sin(x[8]*x[6]**2)+x[6]*x[8]])

start = time.time()
forward = forwardmodevisitor(expression, conditions)
end = time.time()
print(f"Time for FM AD:{end-start}")

#print(f"Derivative of {expression} at {conditions} in FM: {forward}")
# print(f"Derivative of {expression} at {conditions} in RM: {reverse}")


#x0 = expressions.Symbol('x0')
#x1 = expressions.Symbol('x1')
#x2 = expressions.Symbol('x2')
#x3 = expressions.Symbol('x3')
#x4 = expressions.Symbol('x4')
#x5 = expressions.Symbol('x5')
#x6 = expressions.Symbol('x6')
#x7 = expressions.Symbol('x7')
#x8 = expressions.Symbol('x8')
#x9 = expressions.Symbol('x9')
#x = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9]
