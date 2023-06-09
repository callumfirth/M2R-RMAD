from rmad import *
import numpy as np
import time
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
conditions = dict(zip(x, w))  # Note our symbol map, maps the specific x symbol exprs to the value not 'x' value/str

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

def timeRM(expr, conditions):
    start = time.start()
    reverse = reversemodeAD(expression, conditions)
    end = time.time
    return start - end

def timeFM(expr, conditions):
    start = time.start()
    forward = forwardmodevisitor(expression, conditions)
    end = time.time
    return start - end

# print(f"Derivative of {expression} at {conditions} in FM: {forward}")
# print(f"Derivative of {expression} at {conditions} in RM: {reverse}")
