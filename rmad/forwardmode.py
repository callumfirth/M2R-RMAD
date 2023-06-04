from evaluate import _closeto0
import expressions
import numpy as np
from traversal import adjoint, symbolnodes
from functools import singledispatch

def forwardmodevisitor(expr, conditions):
    """Visit an expression in post-order applying a function."""
    stack = [expr]
    visited = {}
    while stack:
        element = stack.pop()
        unvisited_children = []
        for operand in element.operands:
            if operand not in visited:
                unvisited_children.append(operand)
        if unvisited_children:
            stack.append(element)
            for x in unvisited_children:
                stack.append(x)
        else:
            visited[element] = forwardevaluate(element,
                                         *(operand for operand in
                                          element.operands),
                                        symbol_map=conditions)
            element.storedvalue = visited[element]
    return expr.adjoint


@singledispatch
def forwardevaluate(expr, *o, **kwargs):
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


@forwardevaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    value = expr.value
    expr.storedvalue = value
    expr.adjoint = 0
    return value

@forwardevaluate.register(int)
def _(expr, *o, **kwargs):
    value = expr
    expr.storedvalue = value
    return value


@forwardevaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, **kwargs):
    value = symbol_map[expr.value]
    expr.storedvalue = value
    expr.adjoint = 1
    return value


@forwardevaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    value = o[0].storedvalue + o[1].storedvalue
    expr.storedvalue = value
    expr.adjoint = o[0].adjoint + o[1].adjoint
    return value


@forwardevaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    value = o[0].storedvalue - o[1].storedvalue
    expr.storedvalue = value
    expr.adjoint = o[0].adjoint - o[1].adjoint
    return value


@forwardevaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    value = o[0].storedvalue * o[1].storedvalue
    expr.storedvalue = value
    expr.adjoint = o[0].storedvalue*o[1].adjoint + o[1].storedvalue*o[0].adjoint
    return value


@forwardevaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    value = o[0].storedvalue / o[1].storedvalue
    expr.adjoint = (o[0].adjoint*o[1].storedvalue - o[1].adjoint*o[0].storedvalue) / (o[1].storedvalue ** 2)
    return value


@forwardevaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    value = o[0].storedvalue ** o[1].storedvalue
    expr.adjoint = o[1].storedvalue * o[0].storedvalue ** (o[1].storedvalue - 1)
    return value


@forwardevaluate.register(expressions.Sin)
def _(expr, *o, **kwargs):
    value = np.sin(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint = np.cos(o[0].storedvalue) * o[0].adjoint
    return value


@forwardevaluate.register(expressions.Cos)
def _(expr, *o, **kwargs):
    value = np.cos(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint = -np.sin(o[0].storedvalue) * o[0].adjoint
    return value


@forwardevaluate.register(expressions.Exp)
def _(expr, *o, **kwargs):
    value = np.exp(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint = np.exp(o[0].storedvalue) * o[0].adjoint
    return value

@forwardevaluate.register(expressions.Log)
def _(expr, *o, **kwargs):
    value = np.log(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint = (1/o[0].storedvalue) * o[0].adjoint
    return value