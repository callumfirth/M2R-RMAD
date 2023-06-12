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

def test_RMADEexample1():
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    expr = np.asarray([log(z)*exp(x**2), exp(x**2)+sin(x**2 * y)])
    conditions = {x: 2, y: 2, z: 5}
    ans = reversemodeAD(expr, conditions)
    assert np.allclose(ans[x], [2*2*np.exp(2**2)*np.log(5), 
                                2*2*(2*np.cos(2*2**2)+np.exp(2**2))]) and \
        np.allclose(ans[y], [0, np.cos(2*2**2)*2**2]) and \
        np.allclose(ans[z], [np.exp(2**2)/5, 0])
    
def test_FMADEexample1():
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    expr = np.asarray([log(z)*exp(x**2), exp(x**2)+sin(x**2 * y)])
    conditions = {x: 2, y: 2, z: 5}
    ans = forwardmodeAD(expr, conditions)
    assert np.allclose(ans[x], [2*2*np.exp(2**2)*np.log(5), 
                                2*2*(2*np.cos(2*2**2)+np.exp(2**2))]) and \
        np.allclose(ans[y], [0, np.cos(2*2**2)*2**2]) and \
        np.allclose(ans[z], [np.exp(2**2)/5, 0])
