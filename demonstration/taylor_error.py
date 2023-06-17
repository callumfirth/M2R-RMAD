from rmad.reversemode import reversemodeAD
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt
import numpy as np
import rmad.expressions as expressions


def taylor_error(expr, condition, eps, **kwargs):

    # Copy the condition array
    condition_new = dict(condition)
    # Evaluate our expr
    evalpostvisitor(expr, symbol_map=condition)
    # Get our evaluating our expr output
    Jx = expr.storedvalue
    # If our output is a np array get the dimension
    n = len(condition[kwargs['var']])
    # Create a random direction vector and normalise this
    vec = np.random.rand(n)
    vec = np.ones(n)
    # Multiply by our epsilon value

    # Add this new normalised direction vector (of epsilon size) to our initial conditions
    condition_new[kwargs['var']] = condition_new[kwargs['var']] + (vec*eps)
    # Now calculate derivative of our initial conditions
    dJx = np.dot(reversemodeAD(expr, condition)[kwargs['var']], vec*eps)
    # Evaluate expression with these new conditions
    evalpostvisitor(expr, symbol_map=condition_new)
    # Put this evaluated expr into a new array
    Jdeltax = expr.storedvalue
    # Using taylor series expansion find O(eps^2)
    return np.abs(Jdeltax - Jx - dJx)


def taylor_error_plot(expr, condition, eps, **kwargs):
    result = []
    for e in eps:
        result.append(taylor_error(expr, condition, e, **kwargs))
    fig = plt.figure()
    plt.plot(np.log10(np.array(eps)), np.log10(abs(np.mean(np.array(result), axis=1))), label='Taylor error')
    plt.gca().invert_xaxis()
    plt.plot([-2, -9], [-2, -16], linestyle='dashed', label=f'$O(\epsilon^2)$')
    plt.xlabel(f"$\log_{{10}}$ of Epsilon")
    plt.ylabel(f"$\log_{{10}}$ of Taylor error")
    plt.legend()
    plt.show()
    return fig


def convergence_table(expr, condition, eps, **kwargs):
    result = []
    for e in eps:
        result.append(taylor_error(expr, condition, e, **kwargs))
    result = np.array(result)
    result_dif = result[1:]/result[:-1]
    eps_dif = np.array(eps)[1:]/np.array(eps)[:-1]
    grads = np.log(abs(result_dif))/np.log(abs(eps_dif))[:,None]
    points = [f"{eps[i]}-{eps[i+1]}" for i in range(len(eps)-1)]
    d = dict(zip(points, grads))
    f = open("images\\rate_of_convergence.txt", 'w')
    return d
