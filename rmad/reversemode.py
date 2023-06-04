import expressions
from traversal import evalpostvisitor, adjointprevisitor, symbolnodes, adjoint
import numpy as np


def reversemodeAD(expr, conditions):
    """Return dict of the derivatives of expr w.r.t symbols"""
    nodes = []
    symbolnodes(expr, nodes)
    try:
        evalpostvisitor(expr, symbol_map=conditions)
    except ZeroDivisionError:
        raise Exception("Function not valid at initial condition")
    adjointprevisitor(expr)
    symbols = dict()
    for node in nodes:
        symbols[node] = node.adjoint
    return symbols


x = expressions.Symbol('x')
y = expressions.Symbol('y')
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()
#Make sure arrays are float arrays to NaN is supported
a = np.asarray([0., -1])
b = np.asarray([1., 2])
# Mess around with this to see what happens, write any expr and I.V.
conditions = {'x': a, 'y': b}
expression = sin(x**2) + cos(x**2) + exp(y)


print(f"Derivative of {expression} at {conditions} is",
      reversemodeAD(expression, conditions))

#adjoint(expression)

eps = 10**-12
x = expressions.Symbol('x')
conditions = {'x': 2}
expression = x**3 + x
exprdelta = (x + eps)**3 + x + eps
Jx = evalpostvisitor(expression, symbol_map=conditions)
Jdeltax = evalpostvisitor(exprdelta, symbol_map=conditions)
dJx = reversemodeAD(expression, conditions)
# Using taylor series expansion find O(eps^2)
print(f"\nDerivative of {expression} at {conditions} is {dJx}")
result = Jdeltax - Jx - dJx[x]*eps
#print(Jdeltax, Jx, dJx[x], result)
import math
print("Taylor series error:", math.sqrt(result))

# Finite difference method to get error from true derivative (we know is 13)
x = 2
fx = x**3 + x
fxh = (x+eps)**3 + x+eps
df = (fxh-fx)/eps
accdif = 13
print("Finite difference error:", df - accdif)

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