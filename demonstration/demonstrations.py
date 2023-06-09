from rmad import *
import numpy as np
import time
import matplotlib.pyplot as plt


def timeRM(expr, conditions):
    start = time.time()
    reverse = reversemodeAD(expr, conditions)
    end = time.time()
    return end - start


def timeFM(expr, conditions):
    start = time.time()
    forward = forwardmodevisitor(expr, conditions)
    end = time.time()
    return end - start


def generatex(n):
    return [expressions.Symbol(f'x{i}') for i in range(n)]


def generatew(n):
    np.random.seed(0)
    return [np.random.randn(1, 10000) for i in range(n)]


def timex(n):
    x = generatex(n)
    w = generatew(n)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= x[i]
    return [timeFM(expr, conditions), timeRM(expr, conditions)]


def plottime(n):
    nrange = range(1, n+1)
    timelines = np.asarray([timex(n) for n in nrange])
    fig, ax = plt.subplots()
    FM, = ax.plot(nrange, timelines[:, 0], label="Forward Mode")
    RM, = ax.plot(nrange, timelines[:, 1], label="Reverse Mode")
    ax.set_title("Plotting the time to compute derivative of fn=x_1*...*x_n")
    ax.set_ylabel("t: Time to compute function")
    ax.set_xlabel("n: Number of input variables")
    ax.legend()
    return plt.show()


plottime(50)


# print(f"Time for FM AD:{timeRM(expression,conditions)}")
# print(f"Time for RM AD:{timeFM(expression,conditions)}")

# So random arrays are same each time
# Set how many x,y values we want
# n = 10
# Array of initial conditions
# Array of x symbols

# x = generatex(n)
# w = generatew(n)
# sin = expressions.Sin()
# cos = expressions.Cos()
# exp = expressions.Exp()
# log = expressions.Log()
# conditions = dict(zip(x, w))
# expression = np.asarray([log(x[0]**2)*x[9] + 2*x[1]*x[2]*cos(x[3]**4), exp(x[5]**2)*sin(x[8]*x[6]**2)+x[6]*x[8]])

# x = generatex(n)
# sin = expressions.Sin()
# cos = expressions.Cos()
# exp = expressions.Exp()
# log = expressions.Log()
# conditions = dict(zip(x, w))
# expression = np.asarray([log(x[0]**2)*x[9] + 2*x[1]*x[2]*cos(x[3]**4), exp(x[5]**2)*sin(x[8]*x[6]**2)+x[6]*x[8]])

# expression = np.asarray([log(x[0]**2)*x[9] + 2*x[1]*x[2]*cos(x[3]**4), exp(x[5]**2)*sin(x[8]*x[6]**2)+x[6]*x[8]])

# print(f"Time for FM AD:{timeRM(expression,conditions)}")
# print(f"Time for RM AD:{timeFM(expression,conditions)}")

# print(f"Derivative of {expression} at {conditions} in FM: {forward}")
# print(f"Derivative of {expression} at {conditions} in RM: {reverse}")
