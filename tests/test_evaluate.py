import pytest
try:
    from rmad.expressions import Symbol, Number, \
        Add, Sub, Mul, Div, Pow
except ImportError:
    pass


def test_imports():
    from rmad.expressions import Symbol, Number, \
        Add, Sub, Mul, Div, Pow  # NoQA F401


@pytest.fixture
def sample_operand_expr():
    o1 = Symbol('x')
    o2 = Symbol('y')
    o3 = Number(42)
    o4 = Number(1)
    return o1, o2, o3, o4


@pytest.mark.parametrize("a1, a2, expr", [
    (0, 1, "x + y"),
    (2, 1, "42 + y"),
    (2, 3, "42 + 1"),
])
def test_add(a1, a2, expr, sample_operand_expr):
    x, y = sample_operand_expr[a1], sample_operand_expr[a2]
    assert str(Add(x, y)) == expr, \
        f"expected string representation of {expr} but got {str(Add(x, y))}"


@pytest.mark.parametrize("a1, a2, expr", [
    (0, 1, "x - y"),
    (2, 1, "42 - y"),
    (2, 3, "42 - 1"),
])
def test_sub(a1, a2, expr, sample_operand_expr):
    x, y = sample_operand_expr[a1], sample_operand_expr[a2]
    assert str(Sub(x, y)) == expr, \
        f"expected string representation of {expr} but got {str(Sub(x, y))}"


@pytest.mark.parametrize("a1, a2, expr", [
    (0, 1, "x * y"),
    (2, 1, "42 * y"),
    (2, 3, "42 * 1"),
])
def test_mul(a1, a2, expr, sample_operand_expr):
    x, y = sample_operand_expr[a1], sample_operand_expr[a2]
    assert str(Mul(x, y)) == expr, \
        f"expected string representation of {expr} but got {str(Mul(x, y))}"


@pytest.mark.parametrize("a1, a2, expr", [
    (0, 1, "x / y"),
    (2, 1, "42 / y"),
    (2, 3, "42 / 1"),
])
def test_div(a1, a2, expr, sample_operand_expr):
    x, y = sample_operand_expr[a1], sample_operand_expr[a2]
    assert str(Div(x, y)) == expr, \
        f"expected string representation of {expr} but got {str(Div(x, y))}"


@pytest.mark.parametrize("a1, a2, expr", [
    (0, 1, "x ^ y"),
    (2, 1, "42 ^ y"),
    (2, 3, "42 ^ 1"),
])
def test_pow(a1, a2, expr, sample_operand_expr):
    x, y = sample_operand_expr[a1], sample_operand_expr[a2]
    assert str(Pow(x, y)) == expr, \
        f"expected string representation of {expr} but got {str(Pow(x, y))}"


@pytest.fixture
def sample_string_set():
    x = Symbol('x')
    y = Symbol('y')
    tests = [(x + 1)**(y*x**3) + y**2*x*(2 / y),
             (1/x + 1/y)**2 + (1 + 2*x),
             4*(x/y)**(0.5)
             ]
    return tests


@pytest.mark.parametrize("idx, string", [
    (0, '(x + 1) ^ (y * x ^ 3) + y ^ 2 * x * 2 / y'),
    (1, '(1 / x + 1 / y) ^ 2 + 1 + 2 * x'),
    (2, '4 * (x / y) ^ 0.5')
])
def test_str_rep(sample_string_set, idx, string):
    expr = sample_string_set[idx]
    assert str(expr) == string, \
        f"expected string representation of {string} but got {str(expr)}"


@pytest.fixture
def sample_expr_set():
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
def test_any_evaluate(sample_expr_set, idx):
    from tests.expression_tools import postvisitor, evaluate
    expr, x, y, val = sample_expr_set[idx]
    assert postvisitor(expr, evaluate, symbol_map={'x': x, 'y': y}) == val, \
        f"expected an evaluation of {val} for expression {expr}"
