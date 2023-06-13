import pytest
import numpy as np
import rmad.expressions as expressions
from random import randint

try:
    from rmad.forwardmode import forwardmodeAD
except ImportError:
    pass

try:
    from rmad.reversemode import reversemodeAD
except ImportError:
    pass


def test_imports():
    from rmad.evaluate import evaluate # NoQA F401
    from rmad.forwardmode import forwardmodeAD, forwardevaluate # NoQA F401
    from rmad.reversemode import reversemodeAD # NoQA F401
    from rmad.traversal import evalpostvisitor, adjointprevisitor, adjoint, \
        symbolnodes # NoQA F401


@pytest.mark.parametrize("xval,yval", [(1, 1), (np.pi, np.pi),
                                       (randint(0, 100), randint(0, 100))])
def test_RMADEx1(xval, yval):
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: xval, y: yval}
    ans = reversemodeAD(expression, conditions)
    assert np.allclose([ans[x], ans[y]],
                       [np.cos(xval+yval)*xval+np.sin(xval+yval),
                        np.cos(xval+yval)*xval])


@pytest.mark.parametrize("xval,yval", [(1, 1), (np.pi, np.pi),
                                       (randint(0, 100), randint(0, 100))])
def test_FMADEx1(xval, yval):
    x = expressions.Symbol('x')
    sin = expressions.Sin()
    y = expressions.Symbol('y')
    expression = sin(x+y)*x
    conditions = {x: xval, y: yval}
    ans = forwardmodeAD(expression, conditions)
    assert np.allclose([ans[x], ans[y]],
                       [np.cos(xval+yval)*xval+np.sin(xval+yval),
                        np.cos(xval+yval)*xval])


@pytest.mark.parametrize("xval,yval,zval", [(1, 1, 1),
                                            (np.pi, np.pi, np.exp(1)),
                                            (randint(-9, 10),
                                             randint(-99, 100),
                                             randint(1, 100))])
def test_RMADEexample1(xval, yval, zval):
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expr = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    conditions = {x: xval, y: yval, z: zval}
    ans = reversemodeAD(expr, conditions)
    assert np.allclose(
        ans[x], [2*xval*np.exp(xval**2)*np.log(zval),
                 2*xval*(yval*np.cos(yval*xval**2)+np.exp(xval**2))]
        ) and np.allclose(ans[y], [0, np.cos(yval*xval**2)*xval**2]) and \
        np.allclose(ans[z], [np.exp(xval**2)/zval, 0])


@pytest.mark.parametrize("xval,yval,zval", [(1, 1, 1),
                                            (np.pi, np.pi, np.exp(1)),
                                            (randint(-9, 10),
                                             randint(-99, 100),
                                             randint(1, 100))])
def test_FMADEexample1(xval, yval, zval):
    sin = expressions.Sin()
    exp = expressions.Exp()
    log = expressions.Log()
    x = expressions.Symbol('x')
    y = expressions.Symbol('y')
    z = expressions.Symbol('z')
    x2 = x**2
    expx2 = exp(x2)
    expr = np.asarray([log(z)*expx2, expx2+sin(x2 * y)])
    conditions = {x: xval, y: yval, z: zval}
    ans = forwardmodeAD(expr, conditions)
    assert np.allclose(
        ans[x], [2*xval*np.exp(xval**2)*np.log(zval),
                 2*xval*(yval*np.cos(yval*xval**2)+np.exp(xval**2))]
        ) and np.allclose(ans[y], [0, np.cos(yval*xval**2)*xval**2]) and \
        np.allclose(ans[z], [np.exp(xval**2)/zval, 0])
