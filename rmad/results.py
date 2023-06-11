import rmad.expressions as expressions
from rmad.reversemode import reversemodeAD
from rmad.traversal import evalpostvisitor
import rmad.expressions as expressions
import matplotlib.pyplot as plt
import numpy as np
from rmad.taylor_error import taylor_error, taylor_error_plot

x = expressions.Symbol('x')
y = expressions.Symbol('y')
sin = expressions.Sin()
cos = expressions.Cos()
exp = expressions.Exp()
log = expressions.Log()

expr = x*sin(x + y)
conditions = {x:1, y:1}
eps = [10**(-(i+1)) for i in range(10)]

fig = taylor_error_plot(expr, conditions, eps, var=x)
fig.savefig('images\\taylor_error_1.png')

order_of_convergence = np.log(abs(taylor_error(expr, conditions, eps[3], var=x)/taylor_error(expr, conditions, eps[6], var=x)))/np.log(abs(eps[3]/eps[6]))
f = open('images\\rate_of_convergence.txt', 'w')
f.write(str(order_of_convergence))
