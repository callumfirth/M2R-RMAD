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


def evalpostvisitor(expr, **kwargs):
    """Visit an expression in post-order applying a function."""
    stack = [expr]
    visited = {}
    while stack:
        el = stack.pop()
        unvisited_children = []
        for operand in el.operands:
            if operand not in visited:
                unvisited_children.append(operand)
        if unvisited_children:
            stack.append(el)
            for x in unvisited_children:
                stack.append(x)
        else:
            visited[el] = evaluate(el,
                                   *(visited[operand] for operand in
                                     el.operands),
                                   **kwargs)
            el.storedvalue = visited[el]
            if isinstance(el, (expressions.Operator, expressions.Function)):
                el.adjoint = 0
    return visited[expr]


@singledispatch
def reverse_evaluate(expr, *o, **kwargs):
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


@reverse_evaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    return [1]


@reverse_evaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return [1]


@reverse_evaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    return [1, 1]


@reverse_evaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    return [1, -1]


@reverse_evaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    return [expr.operands[1].storedvalue, expr.operands[0].storedvalue]


@reverse_evaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    return [1/expr.operands[1].storedvalue,
            -expr.operands[0].storedvalue/expr.operands[1].storedvalue**2]


@reverse_evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return [(expr.operands[1].storedvalue)
            * expr.operands[0].storedvalue**(expr.operands[1].storedvalue-1),
            expr.operands[0].storedvalue**expr.operands[1].storedvalue
            * math.log(expr.operands[0].storedvalue)]


@reverse_evaluate.register(expressions.Sin)
def _(expr, *o, **kwargs):
    return [math.cos(expr.operands[0].storedvalue)]


@reverse_evaluate.register(expressions.Cos)
def _(expr, *o, **kwargs):
    return [-math.sin(expr.operands[0].storedvalue)]


@reverse_evaluate.register(expressions.Exp)
def _(expr, *o, **kwargs):
    return [math.exp(expr.operands[0].storedvalue)]


@reverse_evaluate.register(expressions.Log)
def _(expr, *o, **kwargs):
    return [1/expr.operands[0].storedvalue]


def adjointprevisitor(expr, fn_adjoint=1, **kwargs):
    """Traverse tree in preorder applying the adjoint to each node.

    Parameters
    ----------
    expr: ExpressionTree
        The expression tree we will traverse.
    fn_parent: float
        The adjoint value of the parent node of expr
    """

    # Set the adjoint of the parent node (initially this is the seed = 1)
    expr.adjoint = fn_adjoint
    # Then visit the children of the parent node and set their adjoints
    for counter, operand in enumerate(expr.operands):
        operand.adjoint += reverse_evaluate(expr)[counter] * expr.adjoint
        adjointprevisitor(operand, operand.adjoint)


def adjoint(tree):
    """Print adjoint values of all the nodes in the tree"""
    print(f"Adjoint: {tree}: {tree.adjoint}")
    for child in tree.operands:
        adjoint(child)


def symbolnodes(tree, nodes):
    if isinstance(tree, expressions.Symbol):
        nodes.append(tree)
    for child in tree.operands:
        symbolnodes(child, nodes)


def reversemodeAD(expr, conditions):
    """Return dict of the derivatives of expr w.r.t symbols"""
    nodes = []
    symbolnodes(expr, nodes)
    try:
        evalpostvisitor(expr, symbol_map=conditions)
    except ZeroDivisionError:
        raise Exception("Function not valid at initial condition")
    adjointprevisitor(expr)
    symbols = dict()
    for node in nodes:
        symbols[node] = node.adjoint
    return symbols


x = expressions.Symbol('x')
y = expressions.Symbol('y')
a = expressions.Symbol('a')

# Mess around with this to see what happens, write any expr and I.V.
conditions = {'x': math.pi, 'y': 1, 'a': 2}
expression = x / expressions.Sin(x)
# adjoint(expr)

print(reversemodeAD(expression, conditions))

eps = 10**-5
x = expressions.Symbol('x')
conditions = {'x': 2}
expression = x**3 + x
exprdelta = (x + eps)**3 + x + eps
Jx = evalpostvisitor(expression, symbol_map=conditions)
Jdeltax = evalpostvisitor(exprdelta, symbol_map=conditions)
dJx = reversemodeAD(expression, conditions)
# Using taylor series expansion find O(eps^2)
result = Jdeltax - Jx - dJx[x]*eps
print(Jdeltax, Jx, dJx[x], result)
print(result)

# Finite difference method to get error from true derivative (we know is 13)
x = 2
fx = x**3 + x
fxh = (x+eps)**3 + x+eps
df = (fxh-fx)/eps
accdif = 13
print(df - accdif)

# Will add a graph but at later date
# import matplotlib.pyplot as plt
# import numpy as np
# x = np.linspace(0, 10, 100)
# y = x**3 + x
#
# fig, ax = plt.subplots()
#
# ax.plot(x, y, linewidth=2.0)
# plt.show
