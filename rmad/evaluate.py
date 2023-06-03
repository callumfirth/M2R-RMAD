from functools import singledispatch
import expressions
import math


@singledispatch
def evaluate(expr, *o, **kwargs):
    """Evaluate an expression node.

    Parameters
    ----------
    expr: Expression
        The expression node to be evaluated.
    *o: numbers.Number
        The results of evaluating the operands of expr.
    **kwargs:
        Any keyword arguments required to evaluate specific types of
        expression.
    symbol_map: dict
        A dictionary mapping Symbol names to numerical values, for
        example:

        {'x': 1}
    """
    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@evaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    return expr.value


@evaluate.register(int)
def _(expr, *o, **kwargs):
    return expr


@evaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return symbol_map[expr.value]


@evaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@evaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@evaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    return o[0] * o[1]


@evaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    return o[0] / o[1]


@evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return o[0] ** o[1]


@evaluate.register(expressions.Sin)
def _(expr, *o, **kwargs):
    return math.sin(o[0])


@evaluate.register(expressions.Cos)
def _(expr, *o, **kwargs):
    return math.cos(o[0])


@evaluate.register(expressions.Exp)
def _(expr, *o, **kwargs):
    return math.exp(o[0])


@evaluate.register(expressions.Log)
def _(expr, *o, **kwargs):
    return math.log(o[0])


@singledispatch
def adjoint_evaluate(expr, *o, **kwargs):
    """Return the adjoint, of the operands of an expression node.
       This is similar to the partial derivative of the expression
       with respect to the operand
    
    Parameters
    ----------
    expr: Expression
        The expression node to return the adjoint children of.
    *o: numbers.Number
        The storedvalue of the expression operands.
    """
    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@adjoint_evaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    return [1]


@adjoint_evaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return [1]


@adjoint_evaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    return [1, 1]


@adjoint_evaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    return [1, -1]


@adjoint_evaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    return [o[1], o[0]]


@adjoint_evaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    return [1/o[1], -o[0]/o[1]**2]


@adjoint_evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return [o[1] * o[0]**(o[1]-1), o[0]**o[1] * math.log(o[0])]


@adjoint_evaluate.register(expressions.Sin)
def _(expr, *o, **kwargs):
    return [math.cos(o[0])]


@adjoint_evaluate.register(expressions.Cos)
def _(expr, *o, **kwargs):
    return [-math.sin(o[0])]


@adjoint_evaluate.register(expressions.Exp)
def _(expr, *o, **kwargs):
    return [math.exp(o[0])]


@adjoint_evaluate.register(expressions.Log)
def _(expr, *o, **kwargs):
    return [1/o[0]]
