import numpy as np
import rmad.expressions as expressions
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt
import numpy.linalg as linalg


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
    B = second_deriv_matrix_maker(n, h) # (I - dt V A + dt D B) = m
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
        m = time_step(C, eval_points, dt)
        C = linalg.solve(m, C)
    plt.show()
    return values_over_time


exp = expressions.Exp()
x = expressions.Symbol('x')
expr = exp(x**2 * -1)


def over_time2(expr, size, numpoints, endtime, dt, V=1, D=1):
    gridpoints = np.linspace(0, size, numpoints)
    evalpostvisitor(expr, symbol_map={x: gridpoints})
    C = expr.storedvalue
    C = np.append(C, np.zeros(8*numpoints))
    C = np.append(np.zeros(numpoints), C)
    gridpoints2 = np.linspace(0, size*10, 10*numpoints)
    timepoints = np.arange(0, endtime, dt)
    values_over_time = [np.array(C)]
    fig, ax = plt.subplots()
    ax.plot(gridpoints2, C)
    for t in range(len(timepoints)):
        m = time_step(C, gridpoints2, dt, V, D)
        C = linalg.solve(m, C)
        values_over_time = np.append(values_over_time, C)
        if t % 10 == 0:
            ax.plot(gridpoints2, C)
    plt.show()
    return values_over_time

def plot_graph(expr, size, numpoints, endtime, dt, V=1, D=1):
    points = over_time2(expr, size, numpoints, endtime, dt, V=1, D=1)
    fig , ax = plt.subplots()
    for t in np.arange(0, endtime, 100*dt):
        print(points)
        ax.plot(points[:, t], np.linspace(0, size*5, numpoints*5))
    plt.show()

x = expressions.Symbol('x')
expr = expressions.Sin(x)**2

print(over_time2(expr, size=np.pi, numpoints=100, endtime=1, dt=0.01, V=10, D=5))

#plot_graph(expr, size=np.pi, numpoints=100, endtime=2, dt=0.001, V=5, D=0.35)