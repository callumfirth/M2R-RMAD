import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as linalg


def first_deriv_matrix_maker(n, h):
    """Creates 1st derivative matrix."""
    array = []
    for i in range(n):
        arr = np.zeros(n)
        if i != 0 and i != n-1:  # Note 1st and Last row is 0 so derivative 0
            arr = np.zeros(n)
            arr[i-1] = -1
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)/(2*h)
    return array


def second_deriv_matrix_maker(n, h):
    """Creates 2nd derivative matrix."""
    array = []
    for i in range(n):
        arr = np.zeros(n)
        if i != 0 and i != n-1:  # Note 1st and Last row is 0 so derivative 0
            arr[i-1] = 1
            arr[i] = -2
            arr[i+1] = 1
        array.append(arr)
    array = np.array(array)/(h**2)
    return array


def matrixM(gridpoints, dt=0.01, V=1, D=1):
    """Create matrix M to use in our solve method."""
    n = len(gridpoints)
    h = gridpoints[1] - gridpoints[0]
    A = first_deriv_matrix_maker(n, h)
    B = second_deriv_matrix_maker(n, h)  # (I - dt V A + dt D B) = m
    m = np.identity(n) + V*A*dt - D*B*dt
    return m


def solve(C, gridpoints, dt, V, D):
    """Solve one time step."""
    M = matrixM(gridpoints, dt, V, D)
    C = linalg.solve(M, C)
    return C


def loop(size, numpoints, endtime, dt, V=1, D=1):
    """Runs PDE till endtime, solving each time step."""
    C = initial_C(size, numpoints)
    gridpoints = np.linspace(0, 10*size, 10*numpoints)
    timepoints = np.arange(0, endtime, dt)
    for t in range(len(timepoints)):
        C = solve(C, gridpoints, dt, V, D)
    return C


def initial_C(func, size=1, numpoints=1000):
    """Create initial condition array using lambda func."""
    gridpoints = np.linspace(0, size, numpoints)
    vfunc = np.vectorize(func)
    return vfunc(gridpoints)


def over_time_plot(size, numpoints, endtime, dt, V=1, D=1):
    """Plot animation for our PDE."""
    ims = []
    gridpoints = np.linspace(0, size, numpoints)
    C = np.sin(gridpoints)**2
    C = np.append(C, np.zeros(8*numpoints))
    C = np.append(np.zeros(numpoints), C)
    gridpoints2 = np.linspace(0, size*10, 10*numpoints)
    timepoints = np.arange(0, endtime, dt)
    values_over_time = [np.array(C)]
    fig, ax = plt.subplots()
    im = ax.plot(gridpoints2, C, "--r")
    for i in range(25):
        ims.append(im)
    for t in range(len(timepoints)):
        values_over_time = np.append(values_over_time, C)
        m = matrixM(gridpoints2, dt, V, D)
        C = linalg.solve(m, C)
        if t % 10 == 0:
            im = ax.plot(gridpoints2, C, color="red",
                         alpha=timepoints[t]/endtime)
            ims.append(im)
    ax.set_xlabel("$x$: Distance")
    ax.set_ylabel("$C$: Concentration")
    plt.show()
