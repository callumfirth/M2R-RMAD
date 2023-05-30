import pytest
from functools import singledispatch
from expressions.expressions import Symbol, Number, \
    Add, Sub, Mul, Div, Pow


class RecursiveError(Exception):
    pass


@singledispatch
def evaluate_test(expr, *o, **kwargs):

    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@evaluate_test.register(Number)
def _(expr, *o, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return expr.value


@evaluate_test.register(Symbol)
def _(expr, *o, symbol_map, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return symbol_map[expr.value]


@evaluate_test.register(Add)
def _(expr, *o, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return o[0] + o[1]


@evaluate_test.register(Sub)
def _(expr, *o, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return o[0] - o[1]


@evaluate_test.register(Mul)
def _(expr, *o, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return o[0] * o[1]


@evaluate_test.register(Div)
def _(expr, *o, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return o[0] / o[1]


@evaluate_test.register(Pow)
def _(expr, *o, **kwargs):
    if hasattr(expr, 'visited'):
        raise RecursiveError("Subexpression already visited!")
    expr.visited = True
    return o[0] ** o[1]


@pytest.fixture
def sample_expr_set():
    from expressions.expressions import Symbol, Number
    x = Symbol('x')
    y = Symbol('y')
    tests = [(3 * x + 2**(y / 5) - 1, 1.5, 10, 7.5),
             (3 * x + 2**(y / 5) - 1, 2.5, 11, 11.09479341998814),
             (4 * x + x**2 * y + 3 * y + 2, 1.0, 2.5, 16),
             (4 * x + x**2 * y + 3 * y + 2, 1.1, 2.25, 15.8725)
             ]
    return tests


@pytest.mark.parametrize("idx", [
    (0),
    (1),
    (2),
    (3)
])
def test_no_recursion_evaluate(sample_expr_set, idx):
    from expressions.expressions import postvisitor
    expr, x, y, val = sample_expr_set[idx]
    assert postvisitor(expr, evaluate_test,
                       symbol_map={'x': x, 'y': y}) == val, \
        f"expected an evaluation of {val} for expression {expr}"
