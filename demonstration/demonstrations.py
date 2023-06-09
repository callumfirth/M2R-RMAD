from matplotlib import colors
import numpy as np
import time
import matplotlib.pyplot as plt
from pde.pde_solver import initial_C
import rmad.expressions as expressions
from rmad.reversemode import reversemodeAD
from rmad.forwardmode import forwardmodeAD
from demonstration.taylor_error import taylor_error, taylor_error_plot
from demonstration.graph_drawer import draw_expression, draw_cluster
from pde.pde_solver import over_time_plot, solve
from rmad.expressions import sin, cos, exp, log


def timerm(expr, conditions):
    start = time.time()
    reversemodeAD(expr, conditions)
    end = time.time()
    return end - start


def timefm(expr, conditions):
    start = time.time()
    forwardmodeAD(expr, conditions)
    end = time.time()
    return end - start


def generatex(n):
    return [expressions.Symbol(f'x_{i}') for i in range(n)]


def generatew(n, m):
    return [np.random.randn(m) for i in range(n)]


def timex1(n, m):
    x = generatex(n)
    w = generatew(n, m)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= x[i]
    return [timefm(expr, conditions), timerm(expr, conditions)]


def timex2(n, m):
    x = generatex(n)
    w = generatew(n, m)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= expressions.Sin(x[i])
    return [timefm(expr, conditions), timerm(expr, conditions)]


def timex3(n, m):
    x = generatex(n)
    w = generatew(n, m)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= expressions.Exp(x[i])
    return [timefm(expr, conditions), timerm(expr, conditions)]


def timex4(n, m):
    x = generatex(n)
    w = generatew(n, m)
    conditions = dict(zip(x, w))
    expr = 1
    for i in range(n):
        expr *= expressions.Log(x[i])
    return [timefm(expr, conditions), timerm(expr, conditions)]


def plottime(n, m, iterations):
    nrange = range(1, n+1)
    timelines1 = 0
    timelines2 = 0
    timelines3 = 0
    timelines4 = 0
    for i in range(iterations):
        print(i)
        timelines1 += np.asarray([timex1(n, m) for n in nrange])
        timelines2 += np.asarray([timex2(n, m) for n in nrange])
        timelines3 += np.asarray([timex3(n, m) for n in nrange])
        timelines4 += np.asarray([timex4(n, m) for n in nrange])
    timelines1 /= iterations
    timelines2 /= iterations
    timelines3 /= iterations
    timelines4 /= iterations
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(7.5, 5))

    fm, = ax1.plot(nrange, timelines1[:, 0], label="Forward Mode")
    rm, = ax1.plot(nrange, timelines1[:, 1], label="Reverse Mode")

    fm, = ax2.plot(nrange, timelines2[:, 0], label="Forward Mode")
    rm, = ax2.plot(nrange, timelines2[:, 1], label="Reverse Mode")

    fm, = ax3.plot(nrange, timelines3[:, 0], label="Forward Mode")
    rm, = ax3.plot(nrange, timelines3[:, 1], label="Reverse Mode")

    fm, = ax4.plot(nrange, timelines4[:, 0], label="Forward Mode")
    rm, = ax4.plot(nrange, timelines4[:, 1], label="Reverse Mode")

    ax1.set_title("Time to compute derivative of $F_1$")
    ax2.set_title("Time to compute derivative of $F_2$")
    ax3.set_title("Time to compute derivative of $F_3$")
    ax4.set_title("Time to compute derivative of $F_4$")

    plt.plot()

    ax1.set_ylabel("$t$: Average time taken")
    ax3.set_ylabel("$t$: Average time taken")
    ax3.set_xlabel("$n$: # of input variables")
    ax4.set_xlabel("$n$: # of input variables")
    plt.legend()
    fig.align_labels()
    fig.tight_layout()
    plt.savefig('images/Graph_TimeDiff.pdf', bbox_inches='tight', pad_inches=0)

    return plt.show()


def rmx1():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: 1, y: 1}
    return reversemodeAD(expression, conditions)


def fmx1():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: 1, y: 1}
    return forwardmodeAD(expression, conditions)


def rmx2():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    expression = np.array([sin(x+y)*x, cos(x)])
    conditions = {x: 1, y: 1}
    return reversemodeAD(expression, conditions)


def fmx2():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    expression = np.array([sin(x+y)*x, cos(x)])
    conditions = {x: 1, y: 1}
    return forwardmodeAD(expression, conditions)


def example_nparray():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expression = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    conditions = {x: 1, y: np.pi, z: 1}
    return reversemodeAD(expression, conditions)


def example_rm():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    x2 = x**2
    expression = sin(y * x2) + exp(x2)
    conditions = {x: 2, y: 2}
    return reversemodeAD(expression, conditions)


def taylor_error_example():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')

    expr = x*sin(x + y)
    conditions = {x: 1, y: 1}
    eps = [10**(-(i+1)) for i in range(10)]

    fig = taylor_error_plot(expr, conditions, eps, var=x)
    try:
        fig.savefig('images\\taylor_error_1.pdf', bbox_inches='tight',
                    pad_inches=0)
        fig.savefig('images\\taylor_error_1.png')
    except FileNotFoundError:
        raise FileNotFoundError(
            "Taylor_Error_Example: Could not save figure: \
                make sure to run shell in .../M2R-RMAD/ folder")
    order_of_convergence = np.log(abs(taylor_error(expr,
                                                   conditions,
                                                   eps[3],
                                                   var=x)
                                      / taylor_error(expr,
                                                     conditions,
                                                     eps[6],
                                                     var=x))) \
        / np.log(abs(eps[3]/eps[6]))
    try:
        f = open('images\\rate_of_convergence.txt', 'w')
        f.write(str(order_of_convergence))
    except FileNotFoundError:
        raise FileNotFoundError(
            "Taylor_Error_Example: Could not save result: \
                 make sure to run shell in .../M2R-RMAD/ folder")


def dag_example1():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expr = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    draw_expression(expr, "Example1")


def dag_example2():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    x2 = x**2
    expr = sin(y * x2) + exp(x2)
    draw_expression(expr, "Example2")


def dag_example2label():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    x2 = x**2
    expr = sin(y * x2) + exp(x2)
    draw_expression(expr, "Example2label", xlab=True, numsymbol=2)


def cluster_graph():
    x_1 = expressions.Symbol('x')
    x_2 = expressions.Symbol('x')
    x_3 = expressions.Symbol('x')
    y_1 = expressions.Symbol('y')
    z_1 = expressions.Symbol('z')
    expr1 = np.asarray([log(z_1)*exp(x_1**2), exp(x_3**2)+sin(x_2**2 * y_1)])
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expr2 = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    draw_cluster(expr1, expr2, "Cluster_1")


def func_nm(n, m):
    x = [expressions.Symbol(f'x_{i}') for i in range(n)]
    expression = np.array([])
    for j in range(m):
        for i in range(n):
            if i == 0:
                subexpr = j*x[i]**j

            else:
                subexpr += j*x[i]**j
        expression = np.append(expression, subexpr)
    conditions = dict(zip(x, generatew(n, 2000)))
    return expression, conditions


def arraytimeRM(n, m):
    # conditions = np.asarray([[dict(zip(generatex(i+1),generatew(i+1, 2)))
    # for i in range(n)] for j in range(m)])
    arr = np.asarray([[timerm(*func_nm(i+1, j+1)) for i in range(n)]
                      for j in range(m)])
    return arr


def arraytimeFM(n, m):
    # conditions = np.asarray([[dict(zip(generatex(i+1), generatew(i+1, 2)))
    # for i in range(n)] for j in range(m)])
    arr = np.asarray([[timefm(*func_nm(i+1, j+1)) for i in range(n)]
                      for j in range(m)])
    return arr


def heatmap(n, m, iterations):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # extent = [1, n, 1, m]
    rmarr = 0
    fmarr = 0
    for i in range(iterations):
        print(i)
        rmarr += arraytimeRM(n, m)
        fmarr += arraytimeFM(n, m)
    rmarr /= iterations
    fmarr /= iterations

    rm = ax1.matshow(rmarr,
                     cmap="hot", origin="lower", interpolation="nearest")
    fm = ax2.matshow(fmarr,
                     cmap="hot", origin="lower", interpolation="nearest")

    norm = colors.CenteredNorm(vcenter=0.0085)
    norm = colors.LogNorm(vmin=0.00005, vmax=0.25)
    rm.set_norm(norm)
    fm.set_norm(norm)
    cbar = plt.colorbar(fm, ax=(ax1, ax2), location="bottom")

    ax1.set_ylabel("m: Number of outputs")
    ax1.set_xlabel("n: Number of inputs")
    ax2.set_xlabel("n: Number of inputs")
    ax1.set_title("Reverse Mode")
    ax2.set_title("Forward Mode")
    cbar.ax.set_xlabel("Average time taken to compute derivative")

    fig.align_labels()
    plt.savefig('images/Graph_HeatMapTimeDiff.pdf',
                bbox_inches='tight',
                pad_inches=0)

    plt.show()


def test():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    expr = x*sin(x*y)
    conditions = {x: 2, y: np.pi}
    rm = reversemodeAD(expr, conditions)
    draw_expression(expr, "Test", xlab=True, numsymbol=2)
    return rm


def pde1_adjoint():
    numpoints = 1000
    size = 10*np.pi
    func = lambda x: np.sin(x)**2 if np.pi < x < 2*np.pi else 0.0
    C0 = initial_C(func, size, numpoints)
    pde = expressions.AdvDif(C0, D=5, V=10, dt=0.01, size=10*np.pi)
    pick = expressions.Pick(None, e=300)
    v = expressions.Symbol('v')
    expr = pde(v)
    expr2 = pick(expr)
    conditions = {v: C0}
    B = reversemodeAD(expr2, conditions)[v]
    points = np.linspace(0, size, numpoints)
    fig, ax = plt.subplots()
    ax.plot(points, B, "--r", label="")
    for j in range(0, 200, 10):
        print(j)
        expr = pde(expr)
        expr2 = pick(expr)
        B = reversemodeAD(expr2, conditions)[v]
        ax.plot(points, B, alpha=j/200, color="red")

    ax.set_xlabel("$x$: Distance")
    ax.set_ylabel("$C$: Concentration")

    plt.show()
    return B


def plotpde():
    over_time_plot(size=np.pi, numpoints=100, endtime=1.5, dt=0.01, V=10, D=5)


def ex222():
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expression = [log(z)*expx2, expx2+sin(x2 * y)][0]
    conditions = {x: 1, y: np.pi, z: 1}
    return reversemodeAD(expression, conditions)


def PDEtaylor_error_new():
    """Simple test for PDE adjoint values"""
    # Number of points
    numpoints = 1000
    # Setting the size
    size = 10*np.pi
    # Setting the function up
    func = lambda x: np.sin(x)**2 if np.pi <= x <= 2*np.pi else 0.0
    # Create initial C, from original func
    C0 = initial_C(func, size, numpoints)
    # Our PDE that we want to use
    pick = expressions.Pick(None, e=130)
    
    # Our symbol
    v = expressions.Symbol('v')
    # Create our expression we want to find adjoint of
    # expr2 = pick(pde(v))
    # Setup values for symbol (we have C0 is array here)
    # conditions = {v: C0}
    # Epsilon values for our taylor error
    eps = [10**(-(i+1)) for i in range(10)]
    # Plot our taylor error
    vals = []
    for ep in eps:
        pde = expressions.AdvDif(C0, D=5, V=10, dt=0.01, size=size)
        expr2 = pick(pde(v))
        gridpoints = np.linspace(0, size, numpoints)
        Jdeltax = solve(solve(C0, gridpoints, dt=ep, V=10, D=5), gridpoints, dt=0.01, V=10, D=5)[130]
        dJx = (reversemodeAD(expr2, {v: C0})[v])[130]*ep
        Jx = expr2.storedvalue
        vals.append(Jdeltax-Jx-dJx)
    fig = plt.figure()
    plt.plot(np.log10(np.array(eps)),
             np.log10(abs(np.array(vals))), label='Taylor error')
    plt.gca().invert_xaxis()
    plt.plot([-2, -9], [-2, -16], linestyle='dashed', label='$O(\epsilon^2)$')
    plt.xlabel("$\log_{{10}}$ of Epsilon")
    plt.ylabel("$\log_{{10}}$ of Taylor error")
    plt.legend()
    plt.show()


def PDEtaylor_error_old():
    """Simple test for PDE adjoint values"""
    # Number of points
    numpoints = 1000
    # Setting the size
    size = 10*np.pi
    # Setting the function up
    func = lambda x: np.sin(x)**2 if np.pi <= x <= 2*np.pi else 0.0
    # Create initial C, from original func
    C0 = initial_C(func, size, numpoints)
    # Our PDE that we want to use
    pick = expressions.Pick(None, e=130)
    pde = expressions.AdvDif(C0, D=5, V=10, dt=0.01, size=size)
    # Our symbol
    v = expressions.Symbol('v')
    # Create our expression we want to find adjoint of
    expr2 = pick(pde(v))
    # Setup values for symbol (we have C0 is array here)
    conditions = {v: C0}
    # Epsilon values for our taylor error
    eps = [10**(-(i+1)) for i in range(10)]
    # Plot our taylor error
    return taylor_error_plot(expr2, conditions, eps, var=v)


def taylor_test_test():
    """Simple test for taylor test"""
    x = expressions.Symbol('x')
    x2 = x**2
    exp = expressions.Exp()
    pick = expressions.Pick(None, 0)
    expression = pick(2*(x2) + cos(x)*(x2)+exp(x))
    w = np.array([1, 2, 5])
    conditions = {x: w}
    eps = [10**(-(i+1)) for i in range(10)]
    return taylor_error_plot(expression, conditions, eps, var=x)


def pick_test():
    """Simple test for taylor test"""
    x = expressions.Symbol('x')
    x2 = x**2
    pick = expressions.Pick(None, 0)
    expression = pick(2*(x2) + (x2))
    w = np.array([3, 5, 3, 7])
    conditions = {x: w}
    return reversemodeAD(expression, conditions)


# print(ex222())

# heatmap(20, 20, 25)

# plottime(50, 20, 25)

# print(rmx1())

# print(fmx1())

# print(rmx2())

# print(fmx2())

# print(example_rm())

# print(example_nparray())

# taylor_error_example()

# dag_example1()

# dag_example2()

# Cluster_Graph()

# dag_example2label()

def reproduce():
    rmx1()  # Unused: RM result on sin(x+y)*x x,y=1
    fmx1()  # Unused: FM result on sin(x+y)*x x,y=1
    plottime(75, 1, 50)  # Plot for timedifference (75 input, 1 deriv, 50 iter)
    example_rm()  # Result for RM algo test in 1D
    example_nparray()  # # Result for RM algo test with arrays
    taylor_error_example()  # Taylor error figure and result
    dag_example1()  # Unused: DAG fig
    dag_example2()  # DAG fig for manual RM algorithm
    cluster_graph()  # Cluster graph figure for comparison

# reproduce() #Please dont run yet, run ones individually above for testing
