import numpy as np
import rmad.expressions as expressions
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt
import numpy.linalg as linalg
import matplotlib.animation as animation

def first_deriv_matrix_maker(n, h):
    array = []
    for i in range(n):
        arr = np.zeros(n)
        if i != 0 and i != n-1:
            arr = np.zeros(n)
            arr[i-1] = -1
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)/(2*h)
    return array


def second_deriv_matrix_maker(n, h):
    array = []
    for i in range(n):
        arr = np.zeros(n)
        if i != 0 and i != n-1:
            arr[i-1] = 1
            arr[i] = -2
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)/(h**2)
    return array


def time_step(C, eval_points, dt=0.1, V=1, D=1):
    n = len(eval_points)
    h = eval_points[1] - eval_points[0]
    A = first_deriv_matrix_maker(n, h)
    B = second_deriv_matrix_maker(n, h)  # (I - dt V A + dt D B) = m
    m = np.identity(n) + V*A*dt - D*B*dt
    return m


def over_time(expr, eval_points, startend, iterations, V=1, D=1, dt=0.001):
    evalpostvisitor(expr, symbol_map={x: eval_points})
    C = expr.storedvalue
    iters = np.linspace(startend[0], startend[1], iterations)
    values_over_time = []
    for i in iters:
        values_over_time.append(C)
        plt.plot(eval_points, C)
        m = time_step(C, eval_points, dt, V, D)
        C = linalg.solve(m, C)
    plt.show()
    return values_over_time


# New Sections


def solve(C, gridpoints, dt, V, D):
    M = time_step(C, gridpoints, dt, V, D)
    C = linalg.solve(M, C)
    return C


def loop(expr, size, numpoints, endtime, dt, V=1, D=1):
    C = initial_C(expr, size, numpoints)
    gridpoints = np.linspace(0, 10*size, 10*numpoints)
    timepoints = np.arange(0, endtime, dt)
    for t in range(len(timepoints)):
        C = solve(C, gridpoints, dt, V, D)
    return C


def initial_C(expr, size=0.1, numpoints=100):
    gridpoints = np.linspace(0, size, numpoints)
    evalpostvisitor(expr, symbol_map={x: gridpoints})
    C = expr.storedvalue
    C = np.append(C, np.zeros(8*numpoints))
    C = np.append(np.zeros(numpoints), C)
    return C


exp = expressions.Exp()
x = expressions.Symbol('x')
expr = exp(x**2 * -1)


# Old Sections
#    gridpoints = np.linspace(0, size, numpoints)
#    evalpostvisitor(expr, symbol_map={x: gridpoints})
#    C = expr.storedvalue
#    C = np.append(C, np.zeros(8*numpoints))
#    C = np.append(np.zeros(numpoints), C)
#    gridpoints2 = np.linspace(0, size*10, 10*numpoints)
#    timepoints = np.arange(0, endtime, dt)
#    values_over_time = [np.array(C)]
#    fig, ax = plt.subplots()
#    im = ax.plot(gridpoints2, C, color="red")
#    for i in range(50):
#        ims.append(im)
#    for t in range(len(timepoints)):
#        values_over_time = np.append(values_over_time, C)
#        m = time_step(C, gridpoints2, dt, V, D)
#        C = linalg.solve(m, C)
#        im = ax.plot(gridpoints2, C, color="red")
#       ims.append(im)


def over_time2(expr, size, numpoints, endtime, dt, V=1, D=1):
    ims = []
    gridpoints = np.linspace(0, size, numpoints)
    evalpostvisitor(expr, symbol_map={x: gridpoints})
    C = expr.storedvalue
    C = np.append(C, np.zeros(8*numpoints))
    C = np.append(np.zeros(numpoints), C)
    gridpoints2 = np.linspace(0, size*10, 10*numpoints)
    timepoints = np.arange(0, endtime, dt)
    values_over_time = [np.array(C)]
    fig, ax = plt.subplots()
    im = ax.plot(gridpoints2, C, color="red")
    for i in range(50):
        ims.append(im)
    for t in range(len(timepoints)):
        values_over_time = np.append(values_over_time, C)
        m = time_step(C, gridpoints2, dt, V, D)
        C = linalg.solve(m, C)
        if t % 10 == 0:
            im = ax.plot(gridpoints2, C, color="red")
            ims.append(im)


    #ani = animation.ArtistAnimation(fig, ims, interval=10, blit=True,
    #                            repeat_delay=100)

    plt.show()

    return C

x = expressions.Symbol('x')
expr = expressions.Sin(x)**2
#A = loop(expr, size=np.pi, numpoints=100, endtime=1.5, dt=0.01, V=10, D=5)
x = expressions.Symbol('x')
expr = expressions.Sin(x)**2
B = over_time2(expr, size=np.pi, numpoints=100, endtime=1.5, dt=0.01, V=10, D=5)

print(B)
# plot_graph(expr, size=np.pi, numpoints=100, endtime=2, dt=0.001, V=5, D=0.35)
