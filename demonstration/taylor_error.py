from rmad.reversemode import reversemodeAD
from rmad.traversal import evalpostvisitor
import matplotlib.pyplot as plt
import numpy as np


def taylor_error(expr, condition, eps, **kwargs):
    condition_new = dict(condition)
    condition_new[kwargs['var']] = condition_new[kwargs['var']] + eps
    evalpostvisitor(expr, symbol_map=condition)
    Jx = expr.storedvalue
    evalpostvisitor(expr, symbol_map=condition_new)
    Jdeltax = expr.storedvalue
    dJx = reversemodeAD(expr, condition)
    # Using taylor series expansion find O(eps^2)
    return abs(Jdeltax - Jx - dJx[kwargs['var']]*eps)


def taylor_error_plot(expr, condition, eps, **kwargs):
    result = []
    for e in eps:
        result.append(taylor_error(expr, condition, e, **kwargs))
    fig = plt.figure()
    plt.plot(np.log10(np.array(eps)), np.log10(abs(np.array(result))))
    plt.gca().invert_xaxis()
    plt.xlabel("Log10 of Epsilon")
    plt.ylabel("Log10 of Taylor error")
    plt.title("Log-Log graph of Epsilon against Taylor error")
    return fig
