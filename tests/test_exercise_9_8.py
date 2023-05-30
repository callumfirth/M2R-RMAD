import pytest
try:
    from expressions.expressions import differentiate
except ImportError:
    pass


def test_diff_import():
    from expressions.expressions import differentiate


@pytest.fixture
def sample_diff_set():
    from expressions.expressions import Symbol
    x = Symbol('x')
    y = Symbol('y')
    Exp = Symbol('Exp')
    tests = [(2 * x + 1, 'x', 1.5, 10, 2, '0.0 * x + 1.0 * 2 + 0.0'),
             (3 * x + y, 'x', 1.5, 10, 3, '0.0 * x + 1.0 * 3 + 0.0'),
             (x * y + x / y, 'y', 3, 2, 2.25,
              '0.0 * y + 1.0 * x + (0.0 * y - x * 1.0) / y ^ 2'),
             (2 * x**3 + x**2 * y, 'x', 2, 3, 36,
              '0.0 * x ^ 3 + 3 * x ^ (3 - 1) * 1.0 * 2 + 2 * x ^'
              ' (2 - 1) * 1.0 * y + 0.0 * x ^ 2'),
              (2 * x + Exp( x ), 'x', 1.5, 10, 2, '0.0 * x + 1.0 * 2 + Exp( x )')
             ]
    return tests


@pytest.mark.parametrize("idx", [
    (0),
    (1),
    (2),
    (3)
])
def test_diff_expr_recursive(sample_diff_set, idx):
    from expressions.expressions import differentiate
    from expression_tools import postvisitor
    expr, dvar, _, _, _, diff_expr = sample_diff_set[idx]
    assert str(postvisitor(expr, differentiate, var=dvar)) == diff_expr, \
        f"expected an expression of {diff_expr}"\
        f" for expression d/d{dvar}({expr})"


@pytest.mark.parametrize("idx", [
    (0),
    (1),
    (2),
    (3)
])
def test_diff_val_recursive(sample_diff_set, idx):
    from expressions.expressions import differentiate
    from expression_tools import postvisitor, evaluate
    expr, dvar, x, y, val, _ = sample_diff_set[idx]
    dexpr = postvisitor(expr, differentiate, var=dvar)
    assert postvisitor(dexpr, evaluate, symbol_map={'x': x, 'y': y}) == val, \
        f"expected a value of {val} for expression d/d{dvar}({expr})" \
        f" evaluated at (x = {x}, y = {y})"


@pytest.mark.parametrize("idx", [
    (0),
    (1),
    (2),
    (3)
])
def test_diff_expr(sample_diff_set, idx):
    from expressions.expressions import postvisitor, differentiate
    expr, dvar, _, _, _, diff_expr = sample_diff_set[idx]
    assert str(postvisitor(expr, differentiate, var=dvar)) == diff_expr, \
        f"expected an expression of {diff_expr}"\
        f" for expression d/d{dvar}({expr})"


@pytest.mark.parametrize("idx", [
    (0),
    (1),
    (2),
    (3)
])
def test_diff_val(sample_diff_set, idx):
    from expressions.expressions import postvisitor, differentiate
    from expression_tools import evaluate
    expr, dvar, x, y, val, _ = sample_diff_set[idx]
    dexpr = postvisitor(expr, differentiate, var=dvar)
    assert postvisitor(dexpr, evaluate, symbol_map={'x': x, 'y': y}) == val, \
        f"expected a value of {val} for expression d/d{dvar}({expr})" \
        f" evaluated at (x = {x}, y = {y})"
