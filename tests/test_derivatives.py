import pytest
import numpy as np
import rmad.expressions as expressions

try:
    from rmad.evaluate import evaluate
except ImportError:
    pass

try:
    from rmad.forwardmode import forwardmodeAD, forwardevaluate
except ImportError:
    pass

try:
    from rmad.reversemode import reversemodeAD
except ImportError:
    pass

try:
    from rmad.traversal import evalpostvisitor, adjointprevisitor, adjoint, \
                            symbolnodes
except ImportError:
    pass

def test_imports():
    from rmad.evaluate import evaluate # NoQA F401
    from rmad.forwardmode import forwardmodeAD, forwardevaluate # NoQA F401
    from rmad.reversemode import reversemodeAD # NoQA F401
    from rmad.traversal import evalpostvisitor, adjointprevisitor, adjoint, \
        symbolnodes # NoQA F401
    
def test_RMADEx1():
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: 1, y: 1}
    ans = reversemodeAD(expression, conditions)
    d1 = ans[x]
    d2 = ans[y]
    assert np.allclose([d1, d2], [0.4931505903, -0.4161468365])

def test_FMADEx1():
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: 1, y: 1}
    ans = forwardmodeAD(expression, conditions)
    d1 = ans[x]
    d2 = ans[y]
    assert np.allclose([d1, d2], [0.4931505903, -0.4161468365])
