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


x0 = expressions.Symbol('x0')
x1 = expressions.Symbol('x1')
x2 = expressions.Symbol('x2')
x3 = expressions.Symbol('x3')
x4 = expressions.Symbol('x4')
x5 = expressions.Symbol('x5')
x6 = expressions.Symbol('x6')
x7 = expressions.Symbol('x7')
x8 = expressions.Symbol('x8')
x9 = expressions.Symbol('x9')
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()
#Make sure arrays are float arrays to NaN is supported
np.random.seed(0)
w0 = np.random.randn(1,100000)
w1 = np.random.randn(1,100000)
w2 = np.random.randn(1,100000)
w3 = np.random.randn(1,100000)
w4 = np.random.randn(1,100000)
w5 = np.random.randn(1,100000)
w6 = np.random.randn(1,100000)
w7 = np.random.randn(1,100000)
w8 = np.random.randn(1,100000)
w9 = np.random.randn(1,100000)

# Mess around with this to see what happens, write any expr and I.V.
conditions = {x0:w0, x1:w1, x2:w2, x3:w3, x4:w4, x5:w5, x6:w6, x7:w7, x8:w8, x9:w9}  # Note our symbol map, maps the specific x symbol exprs to the value not 'x' value/str
expression = np.asarray([log(x0**2)*x9 + 2*x1*x2*cos(x3**4), exp(x4**2)*sin(x5*x6**2)+x7*x8])

# Need to fix to allow np arrays in expr instead of just in the conditions

start = time.time()
reverse = reversemodeAD(expression, conditions)
#print(f"Derivative of {expression} at {conditions} in RM: {reverse}")
end = time.time()
print(f"Time for RM AD:{end-start}")
#adjoint(expression)

x0 = expressions.Symbol('x0')
x1 = expressions.Symbol('x1')
x2 = expressions.Symbol('x2')
x3 = expressions.Symbol('x3')
x4 = expressions.Symbol('x4')
x5 = expressions.Symbol('x5')
x6 = expressions.Symbol('x6')
x7 = expressions.Symbol('x7')
x8 = expressions.Symbol('x8')
x9 = expressions.Symbol('x9')
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()
conditions = {x0:w0, x1:w1, x2:w2, x3:w3, x4:w4, x5:w5, x6:w6, x7:w7, x8:w8, x9:w9}
#Need to fix fm to work with np arrays
expression = np.asarray([log(x0**2)*x9 + 2*x1*x2/cos(x3**4), exp(x4**2)/sin(x5*x6**2)+x7*x8])


start = time.time()
forward = forwardmodevisitor(expression, conditions)
#print(f"Derivative of {expression} at {conditions} in FM: {forward}")
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