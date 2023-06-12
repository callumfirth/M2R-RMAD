import rmad.expressions as expressions
import numpy as np
from functools import singledispatch

def forwardmodeAD(expr, conditions):
    """Visit an expression in post-order applying a function."""
    adjoints = dict()
    for symbol in conditions.keys():

        # Returns stack of output expr (so works for arrays)
        stack = []
        if isinstance(expr, np.ndarray):
            for expression in expr:
                stack.append(expression)
        else:
            stack = [expr]

        # The actual forwardmode func
        visited = {}
        while stack:
            element = stack.pop()
            element.adjoint = 0
            unvisited_children = []
            for operand in element.operands:
                if operand not in visited:
                    unvisited_children.append(operand)
            if unvisited_children:
                stack.append(element)
                for x in unvisited_children:
                    stack.append(x)
            else:
                visited[element] = forwardevaluate(element, symbol,
                                                *(operand for operand in
                                                element.operands),
                                            symbol_map=conditions)
                element.storedvalue = visited[element]

        #Returns adjoint of each expression in our expr (so works for arrays)
        adjointlist = []
        if isinstance(expr, np.ndarray):
            for expression in expr:
                adjointlist.append(expression.adjoint)
        else:
            adjointlist = [expr.adjoint]
        adjoints[symbol] = adjointlist
    return adjoints


@singledispatch
def forwardevaluate(expr, seed, *o, **kwargs):
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
def _(expr, seed, *o, **kwargs):
    value = expr.value
    expr.storedvalue = value
    expr.adjoint += 0
    return value

@forwardevaluate.register(int)
def _(expr, seed, *o, **kwargs):
    value = expr
    expr.storedvalue = value
    expr.adjoint += 0
    return value


@forwardevaluate.register(expressions.Symbol)
def _(expr, seed, *o, symbol_map, **kwargs):
    value = symbol_map[expr]
    expr.storedvalue = value
    expr.adjoint += 0
    if seed == expr:
        expr.adjoint += 1
    return value


@forwardevaluate.register(expressions.Add)
def _(expr, seed, *o, **kwargs):
    value = o[0].storedvalue + o[1].storedvalue
    expr.storedvalue = value
    expr.adjoint += o[0].adjoint + o[1].adjoint
    return value


@forwardevaluate.register(expressions.Sub)
def _(expr, seed, *o, **kwargs):
    value = o[0].storedvalue - o[1].storedvalue
    expr.storedvalue = value
    expr.adjoint += o[0].adjoint - o[1].adjoint
    return value


@forwardevaluate.register(expressions.Mul)
def _(expr, seed, *o, **kwargs):
    value = o[0].storedvalue * o[1].storedvalue
    expr.storedvalue = value
    expr.adjoint += o[0].storedvalue*o[1].adjoint + o[1].storedvalue*o[0].adjoint
    return value


@forwardevaluate.register(expressions.Div)
def _(expr, seed, *o, **kwargs):
    value = o[0].storedvalue / o[1].storedvalue
    expr.adjoint += (o[0].adjoint*o[1].storedvalue - o[1].adjoint*o[0].storedvalue) / (o[1].storedvalue ** 2)
    return value


@forwardevaluate.register(expressions.Pow)
def _(expr, seed, *o, **kwargs):
    value = o[0].storedvalue ** o[1].storedvalue
    expr.adjoint += o[0].adjoint * o[1].storedvalue * o[0].storedvalue ** (o[1].storedvalue - 1)
    return value


@forwardevaluate.register(expressions.Sin)
def _(expr, seed, *o, **kwargs):
    value = np.sin(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint += np.cos(o[0].storedvalue) * o[0].adjoint
    return value


@forwardevaluate.register(expressions.Cos)
def _(expr, symbol, *o, **kwargs):
    value = np.cos(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint += -np.sin(o[0].storedvalue) * o[0].adjoint
    return value


@forwardevaluate.register(expressions.Exp)
def _(expr, symbol, *o, **kwargs):
    value = np.exp(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint += np.exp(o[0].storedvalue) * o[0].adjoint
    return value

@forwardevaluate.register(expressions.Log)
def _(expr, symbol, *o, **kwargs):
    value = np.log(o[0].storedvalue)
    expr.storedvalue = value
    expr.adjoint += (1/o[0].storedvalue) * o[0].adjoint
    return value
