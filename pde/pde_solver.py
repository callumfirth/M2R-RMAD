import numpy as np
import rmad.expressions as expressions
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt


def first_deriv_matrix_maker(n):
    array = []
    for i in range(n):
        arr = np.zeros(n)
        if i != 0 and i != n-1:
            arr = np.zeros(n)
            arr[i-1] = -1
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)
    return array


def second_deriv_matrix_maker(n):
    array = []
    for i in range(n):
        arr = np.zeros(n)
        if i != 0 and i != n-1:
            arr[i-1] = 1
            arr[i] = -2
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)
    return array


def time_step(C, eval_points, V=1, D=1):
    n = len(eval_points)
    A = first_deriv_matrix_maker(n)
    B = second_deriv_matrix_maker(n)
    h = eval_points[1] - eval_points[0]
    dc = -(V * np.matmul(A, C)/(2*h)) + D*np.matmul(B, C)/(h**2)
    return dc


def over_time(expr, eval_points, startend, iterations, V=1, D=1):
    evalpostvisitor(expr, symbol_map={x: eval_points})
    C = expr.storedvalue
    iters = np.linspace(startend[0], startend[1], iterations)
    values_over_time = []
    for i in iters:
        values_over_time.append(C)
        plt.plot(eval_points, C)
        C = C + time_step(C, eval_points, V, D)
    return values_over_time


exp = expressions.Exp()
x = expressions.Symbol('x')
expr = exp(x**2 * -1)

#over_time(expr, np.linspace(-1, 1, 200), (0, 2), 200)


def over_time2(expr, size, numpoints, endtime, dt, V=1, D=1):
    gridpoints = np.linspace(0, size, numpoints)
    evalpostvisitor(expr, symbol_map={x: gridpoints})
    C = expr.storedvalue
    C = np.append(C, np.zeros(4*numpoints))
    gridpoints2 = np.linspace(0, size*5, 5*numpoints)
    timepoints = np.arange(0, endtime, dt)
    values_over_time = [np.array(C)]
    fig, ax = plt.subplots()
    for t in timepoints:
        C = C + time_step(C, gridpoints2, V, D)*dt
        values_over_time = np.append(values_over_time, C)
        if t in np.arange(0, endtime, dt*100):
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

print(over_time2(expr, size=np.pi, numpoints=100, endtime=2, dt=0.001, V=5, D=0.35))

#plot_graph(expr, size=np.pi, numpoints=100, endtime=2, dt=0.001, V=5, D=0.35)