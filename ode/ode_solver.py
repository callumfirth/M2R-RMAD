import numpy as np
import rmad.expressions as expressions
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt


def first_deriv_matrix_maker(n):
    array = []
    for i in range(n):
        if i == 0:
            arr = np.array([0, 1] + [0 for i in range(n-2)])
        elif i == n-1:
            arr = np.array([0 for i in range(n-2)] + [-1, 0])
        else:
            arr = np.zeros(n)
            arr[i-1] = -1
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)
    return array


def second_deriv_matrix_maker(n):
    array = []
    for i in range(n):
        if i == 0:
            arr = np.array([-2, 1] + [0 for i in range(n-2)])
        elif i == n-1:
            arr = np.array([0 for i in range(n-2)] + [1, -2])
        else:
            arr = np.zeros(n)
            arr[i-1] = 1
            arr[i] = -2
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)
    return array


def evaluating_points(expr, eval_points):
    evaluated_points = []
    for i in eval_points:
        conditions = {x: i}
        evalpostvisitor(expr, symbol_map=conditions)
        evaluated_points.append(expr.storedvalue)
    return evaluated_points


def time_step(C, eval_points, V=1, D=1):
    n = len(eval_points)
    A = first_deriv_matrix_maker(n)
    B = second_deriv_matrix_maker(n)
    h = eval_points[1] - eval_points[0]
    dc = -(V * np.matmul(A, C)/(2*h)) + D*np.matmul(B, C)/(h**2)
    print(dc)
    return dc


def over_time(expr, eval_points, startend, iterations, V=1, D=1):
    C = evaluating_points(expr, eval_points)
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


over_time(expr, np.linspace(-1, 1, 200), (0, 2), 200)