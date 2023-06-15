from rmad.reversemode import reversemodeAD
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt
import numpy as np
import rmad.expressions as expressions


def taylor_error(expr, condition, eps, **kwargs):
    condition_new = dict(condition)
    evalpostvisitor(expr, symbol_map=condition)
    Jx = expr.storedvalue
    if isinstance(Jx, np.ndarray):
        n = len(Jx)
    else:
        n = 1
    Jx = np.array(Jx)
    vec = np.random.rand(n)
    vec = vec/np.linalg.norm(vec)
    condition_new[kwargs['var']] = condition_new[kwargs['var']] + (eps * vec)
    evalpostvisitor(expr, symbol_map=condition_new)
    Jdeltax = np.array(expr.storedvalue)
    dJx = np.array(reversemodeAD(expr, condition)[kwargs['var']])
    # Using taylor series expansion find O(eps^2)
    print(Jdeltax - Jx)
    return np.abs(Jdeltax - Jx - dJx*eps)


def taylor_error_plot(expr, condition, eps, **kwargs):
    result = []
    for e in eps:
        result.append(taylor_error(expr, condition, e, **kwargs))
    fig = plt.figure()
    plt.plot(np.log10(np.array(eps)), np.log10(abs(np.array(result))), label='Taylor error')
    plt.gca().invert_xaxis()
    plt.plot([-2, -9], [-2, -16], linestyle='dashed', label=f'$O(\epsilon^2)$')
    plt.xlabel("Log10 of Epsilon")
    plt.ylabel("Log10 of Taylor error")
    return fig


def convergence_table(expr, condition, eps, **kwargs):
    result = []
    for e in eps:
        result.append(taylor_error(expr, condition, e, **kwargs))
    result = np.array(result)
    result_dif = result[1:]/result[:-1]
    eps_dif = np.array(eps)[1:]/np.array(eps)[:-1]
    grads = np.log(abs(result_dif))/np.log(abs(eps_dif))
    points = [f"{i+1}-{i+2}" for i in range(len(eps)-1)]
    d = dict(zip(points, grads))
    f = open("images\\rate_of_convergence.txt", 'w')
    return d


x = expressions.Symbol('x')
y = expressions.Symbol('y')
sin = expressions.Sin()

expr = x*sin(x + y)
conditions = {x: 1, y: 1}
eps = [10**(-(i+1)) for i in range(10)]

print(convergence_table(expr, conditions, eps, var=x))
