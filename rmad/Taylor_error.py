from reversemode import reversemodeAD
from traversal import evalpostvisitor
import expressions
import matplotlib.pyplot as plt
import numpy as np

eps = [10**-(i+1) for i in range(10)]
result = []
for i in range(len(eps)):
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    conditions = {'x': 1, 'y': 1}
    expression = x*sin(x+y)
    exprdelta = (x + eps[i])*sin(x + eps[i] + y)
    Jx = evalpostvisitor(expression, symbol_map=conditions)
    Jdeltax = evalpostvisitor(exprdelta, symbol_map=conditions)
    dJx = reversemodeAD(expression, conditions)
    # Using taylor series expansion find O(eps^2)
    result.append(Jdeltax - Jx - dJx[x]*eps[i])

plt.plot(np.log10(np.array(eps)), np.log10(abs(np.array(result))))
plt.gca().invert_xaxis()
plt.xlabel("Log10 of Epsilon")
plt.ylabel("Log10 of Taylor error")
plt.title("Log-Log graph of Epsilon against Taylor error")
plt.show()
plt.clf()

eps = [10**-(i+1) for i in range(10)]
result = []
for i in range(len(eps)):
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    conditions = {'x': 1, 'y': 1}
    expression = x*sin(x+y)
    exprdelta = (x + eps[i])*sin(x + eps[i] + y)
    exprnegdelta = (x - eps[i])*sin(x - eps[i] + y)
    Jx = evalpostvisitor(exprnegdelta, symbol_map=conditions)
    Jdeltax = evalpostvisitor(exprdelta, symbol_map=conditions)
    dJx = reversemodeAD(expression, conditions)
    print((Jdeltax - Jx)/(2*eps[i]))
    # Using taylor series expansion find O(eps^2)
    result.append((Jdeltax - Jx)/(2*eps[i]) - dJx[x])

plt.plot(np.log10(abs(np.array(eps))), np.log10(abs(np.array(result))))
plt.gca().invert_xaxis()
plt.xlabel("Log10 of Epsilon")
plt.ylabel("Log10 of Finite Difference error")
plt.title("Log-Log graph of Epsilon against Finite Difference error")
plt.show()

