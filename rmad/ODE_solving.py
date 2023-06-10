import numpy as np
import numpy.linalg as linalg

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


print(first_deriv_matrix_maker(5))
print(second_deriv_matrix_maker(5))