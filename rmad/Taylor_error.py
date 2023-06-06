from reversemode import reversemodeAD
from traversal import evalpostvisitor
import expressions
import matplotlib.pyplot as plt
import numpy as np

eps = [10**-(i+1) for i in range(10)]
result = []
for i in range(len(eps)):
    x = expressions.Symbol('x')
    conditions = {'x': 2}
    expression = x**3 + x
    exprdelta = (x + eps[i])**3 + x + eps[i]
    Jx = evalpostvisitor(expression, symbol_map=conditions)
    Jdeltax = evalpostvisitor(exprdelta, symbol_map=conditions)
    dJx = reversemodeAD(expression, conditions)
    # Using taylor series expansion find O(eps^2)
    result.append(Jdeltax - Jx - dJx[x]*eps[i])

plt.plot(np.log10(np.array(eps)), np.log10(np.array(result)))
plt.gca().invert_xaxis()
plt.xlabel("Log10 of Epsilon")
plt.ylabel("Log10 of Taylor error")
plt.title("Log-Log graph of Epsilon against Taylor error")
plt.show()