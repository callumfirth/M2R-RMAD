import numpy as np
import time
import matplotlib.pyplot as plt
from rmad import *
import rmad.expressions as expressions
from rmad.reversemode import reversemodeAD
from rmad.forwardmode import forwardmodeAD
from demonstration.taylor_error import taylor_error, taylor_error_plot
from demonstration.graph_drawer import draw_expression, draw_cluster

def timeRM(expr, conditions):
    start = time.time()
    reverse = reversemodeAD(expr, conditions)
    end = time.time()
    return end - start


def timeFM(expr, conditions):
    start = time.time()
    forward = forwardmodeAD(expr, conditions)
    end = time.time()
    return end - start


def generatex(n):
    return [expressions.Symbol(f'x{i}') for i in range(n)]


def generatew(n):
    np.random.seed(0)
    return [np.random.randn(1, 1000) for i in range(n)]


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

    plt.plot()

    ax1.set_ylabel("t: Time taken to compute derivative")
    ax3.set_ylabel("t: Time taken to compute derivative")
    ax3.set_xlabel("n: Number of input variables")
    ax4.set_xlabel("n: Number of input variables")
    plt.legend()
    fig.align_labels()
    fig.tight_layout()
    plt.savefig('Graph_TimeDiff.pdf', bbox_inches='tight', pad_inches=0)

    return plt.show()


def RMADEx1():
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: 1, y: 1}
    return reversemodeAD(expression, conditions)


def FMADEx1():
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: 1, y: 1}
    return forwardmodeAD(expression, conditions)


def example1():
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expression = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    conditions = {x: 1, y: np.pi, z: 1}
    return reversemodeAD(expression, conditions)

def example2():
    sin = expressions.Sin()
    exp = expressions.Exp()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    x2 = x**2
    expression = sin(y * x2) + exp(x2)
    conditions = {x: 2, y: 2}
    return reversemodeAD(expression, conditions)


def taylor_error_example():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    sin = expressions.Sin()

    expr = x*sin(x + y)
    conditions = {x: 1, y: 1}
    eps = [10**(-(i+1)) for i in range(10)]

    fig = taylor_error_plot(expr, conditions, eps, var=x)
    try:
        fig.savefig('images\\taylor_error_1.png')
    except:
        print("Taylor_Error_Example: Could not save figure: Path not found, make sure to run shell in .../M2R-RMAD/ folder")
    order_of_convergence = np.log(abs(taylor_error(expr, conditions, eps[3], var=x)/taylor_error(expr, conditions, eps[6], var=x)))/np.log(abs(eps[3]/eps[6]))
    try:
        f = open('images\\rate_of_convergence.txt', 'w')
        f.write(str(order_of_convergence))
    except:
        print("Taylor_Error_Example: Could not save result: Path not found, make sure to run shell in .../M2R-RMAD/ folder")


def DAG_example1():
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expr = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    draw_expression(expr, "Example1")


def DAG_example2():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    sin = expressions.Sin()
    exp = expressions.Exp()
    x2 = x**2
    expr = sin(y * x2) + exp(x2)
    draw_expression(expr, "Example2")


def Cluster_Graph():
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x_1 = expressions.Symbol('x')
    x_2 = expressions.Symbol('x')
    x_3 = expressions.Symbol('x')
    y_1 = expressions.Symbol('y')
    z_1 = expressions.Symbol('z')
    expr1 = np.asarray([log(z_1)*exp(x_1**2), exp(x_3**2)+sin(x_2**2 * y_1)])
    sin2 = expressions.Sin()
    exp2 = expressions.Exp()
    log2 = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp2(x2)
    expr2 = np.asarray([log2(z)*expx2, expx2+sin2(x2 * y)])
    draw_cluster(expr1, expr2, "Cluster_1")


plottime(75)

# print(RMADEx1())

# print(FMADEx1())

# print(example1())

# print(example2())

# taylor_error_example()

# DAG_example1()

# DAG_example2()

# Cluster_Graph()





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
