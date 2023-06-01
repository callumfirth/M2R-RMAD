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
        element = stack.pop()
        unvisited_children = []
        for operand in element.operands:
            if operand not in visited:
                unvisited_children.append(operand)
        if unvisited_children:
            stack.append(element)
            for x in unvisited_children:
                stack.append(x)
        else:  # Need to modify this to stores tuple? with val and adjoint
            visited[element] = evaluate(element,
                                        *(visited[operand] for operand in
                                          element.operands),
                                        **kwargs)
            element.storedvalue = visited[element]
    return visited[expr]

x = expressions.Symbol('x')

y = expressions.Symbol('y')

expr = 3*x + 2**(y/5) - 1

evalpostvisitor(expr, symbol_map={'x': 1.5, 'y': 10})

print(evalpostvisitor(expressions.Sin(x), symbol_map={'x': math.pi, 'y': 10}))
print(evalpostvisitor(2 * x + expressions.Cos(2 * x), symbol_map={'x': 1.5, 'y': 10}))
print(repr(evalpostvisitor(2 * x + expressions.Cos(2 * x), symbol_map={'x': 1.5, 'y': 10})))
print(evalpostvisitor(2 * x + expressions.Exp(x ** 2), symbol_map={'x': 1.5, 'y': 10}))

def previsitor(tree, **kwargs, fn_parent=None):
    """Traverse tree in preorder applying a function to every node.

    Parameters
    ----------
    tree: TreeNode
        The tree to be visited.
    fn: function(node, fn_parent)
        A function to be applied at each node. The function should take
        the node to be visited as its first argument, and the result of
        visiting its parent as the second.
    """
    fn_out = evaluate(tree, fn_parent, symbol_map=kwargs)

    for child in tree.children:
        previsitor(child, evaluate, kwargs, fn_out)

expr = x**2 + 5*x

previsitor(expr, evaluate, symbol_map={'x':1.5})