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


def timex1(n):
    x = generatex(n)
    w = generatew(n)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= x[i]
    return [timeFM(expr, conditions), timeRM(expr, conditions)]


def timex2(n):
    x = generatex(n)
    w = generatew(n)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= expressions.Sin(x[i])
    return [timeFM(expr, conditions), timeRM(expr, conditions)]


def timex3(n):
    x = generatex(n)
    w = generatew(n)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= expressions.Exp(x[i])
    return [timeFM(expr, conditions), timeRM(expr, conditions)]


def timex4(n):
    x = generatex(n)
    w = generatew(n)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= expressions.Log(x[i])
    return [timeFM(expr, conditions), timeRM(expr, conditions)]


def plottime(n):
    nrange = range(1, n+1)
    timelines1 = np.asarray([timex1(n) for n in nrange])
    timelines2 = np.asarray([timex2(n) for n in nrange])
    timelines3 = np.asarray([timex3(n) for n in nrange])
    timelines4 = np.asarray([timex4(n) for n in nrange])
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(15,10))
    
    FM, = ax1.plot(nrange, timelines1[:, 0], label="Forward Mode")
    RM, = ax1.plot(nrange, timelines1[:, 1], label="Reverse Mode")

    FM, = ax2.plot(nrange, timelines2[:, 0], label="Forward Mode")
    RM, = ax2.plot(nrange, timelines2[:, 1], label="Reverse Mode")

    FM, = ax3.plot(nrange, timelines3[:, 0], label="Forward Mode")
    RM, = ax3.plot(nrange, timelines3[:, 1], label="Reverse Mode")

    FM, = ax4.plot(nrange, timelines4[:, 0], label="Forward Mode")
    RM, = ax4.plot(nrange, timelines4[:, 1], label="Reverse Mode")

    ax1.set_title("Plotting the time to compute derivative of fn_1")
    ax2.set_title("Plotting the time to compute derivative of fn_2")
    ax3.set_title("Plotting the time to compute derivative of fn_3")
    ax4.set_title("Plotting the time to compute derivative of fn_4")

    ax1.set_ylabel("t: Time taken to compute derivative")
    ax3.set_ylabel("t: Time taken to compute derivative")
    ax3.set_xlabel("n: Number of input variables")
    ax4.set_xlabel("n: Number of input variables")
    plt.legend()
    fig.align_labels()
    fig.tight_layout()
    plt.savefig('image.pdf', bbox_inches='tight', pad_inches=0)

    return plt.show()


plottime(10)


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
