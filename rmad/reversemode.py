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


x = expressions.Symbol('x')
y = expressions.Symbol('y')
z = expressions.Symbol('z')
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()
#Make sure arrays are float arrays to NaN is supported
np.random.seed(0)
a = 2
b = 2
c = 3
# Mess around with this to see what happens, write any expr and I.V.
conditions = {x: a, y: b} # Note our symbol map, maps the specific x symbol exprs to the value not 'x' value/str
expression = np.asarray([x**2 + 2*x*y, sin(x**2)])

# Need to fix to allow np arrays in expr instead of just in the conditions

start = time.time()
reverse = reversemodeAD(expression, conditions)
print(f"Derivative of {expression} at {conditions} in RM: {reverse}")
end = time.time()
print(f"Time for RM AD:{end-start}")
#adjoint(expression)

x = expressions.Symbol('x')
y = expressions.Symbol('y')
z = expressions.Symbol('z')
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()

#Need to fix fm to work with np arrays
expression = sin(x)

start = time.time()
conditions = {x: a, y: b}
forward = forwardmodevisitor(expression, conditions)
print(f"Derivative of {expression} at {conditions} in FM: {forward}")
end = time.time()
print(f"Time for FM AD:{end-start}")
#adjoint(expression)



# eps = 10**-12
# x = expressions.Symbol('x')
# conditions = {'x': 2}
# expression = x**3 + x
# exprdelta = (x + eps)**3 + x + eps
# Jx = evalpostvisitor(expression, symbol_map=conditions)
# Jdeltax = evalpostvisitor(exprdelta, symbol_map=conditions)
# dJx = reversemodeAD(expression, conditions)
# Using taylor series expansion find O(eps^2)
# print(f"\nDerivative of {expression} at {conditions} is {dJx}")
# result = Jdeltax - Jx - dJx[x]*eps
# print(Jdeltax, Jx, dJx[x], result)
# import math
# print("Taylor series error:", math.sqrt(result))

# Finite difference method to get error from true derivative (we know is 13)
# x = 2
# fx = x**3 + x
# fxh = (x+eps)**3 + x+eps
# df = (fxh-fx)/eps
# accdif = 13
# print("Finite difference error:", df - accdif)
#
# Will add a graph but at later date
# import matplotlib.pyplot as plt
# import numpy as np
# x = np.linspace(0, 10, 100)
# y = x**3 + x
#
# fig, ax = plt.subplots()
#
# ax.plot(x, y, linewidth=2.0)
# plt.show