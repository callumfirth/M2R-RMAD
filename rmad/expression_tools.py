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
            visited[element] = evaluate(element,
                                        *(visited[operand] for operand in
                                          element.operands),
                                        **kwargs)
            element.storedvalue = visited[element]
            if isinstance(element, expressions.Operator) or isinstance(element, expressions.Function):
                element.adjoint = 0
    return visited[expr]

#x = expressions.Symbol('x')

#y = expressions.Symbol('y')

#expr = 3*x + 2**(y/5) - 1

#evalpostvisitor(expr, symbol_map={'x': 1.5, 'y': 10})

#print(evalpostvisitor(expressions.Sin(x), symbol_map={'x': math.pi, 'y': 10}))
#print(evalpostvisitor(2 * x + expressions.Cos(2 * x), symbol_map={'x': 1.5, 'y': 10}))
#print(repr(evalpostvisitor(2 * x + expressions.Cos(2 * x), symbol_map={'x': 1.5, 'y': 10})))
#print(evalpostvisitor(2 * x + expressions.Exp(x ** 2), symbol_map={'x': 1.5, 'y': 10}))

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
    return [o[0] / o[1]]

@reverse_evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return [(expr.operands[1].storedvalue)*expr.operands[0].storedvalue**(expr.operands[1].storedvalue-1),
            expr.operands[0].storedvalue**expr.operands[1].storedvalue*math.log(expr.operands[0].storedvalue)]

@reverse_evaluate.register(expressions.Sin)
def _(expr, *o, **kwargs):
    return [math.cos(expr.operands[0].storedvalue)]

@reverse_evaluate.register(expressions.Cos)
def _(expr, *o, **kwargs):
    return -math.sin(o[0]) * o[1]

@reverse_evaluate.register(expressions.Exp)
def _(expr, *o, **kwargs):
    return math.exp(o[0]) * o[1]

@reverse_evaluate.register(expressions.Log)
def _(expr, *o, **kwargs):
    return o[1] / o[0]

def previsitor(expr, fn_parent=None, **kwargs):
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

    # Initially we do postvisitor (forward traverse) the tree to get the value of the parent node
    # This should be already run before previsitor is ran
    # fn_parent = evalpostvisitor(eval, **kwargs)
    
    #Get the adjoint of the parent node (this is the seed and is set to 1)
    if not fn_parent:
        expr.adjoint = 1
    
    #We then need to visit the children of the parent node and set their adjoints
    for counter, operand in enumerate(expr.operands):
        operand.adjoint += reverse_evaluate(expr)[counter] * expr.adjoint
        previsitor(operand, operand.adjoint)
    

x = expressions.Symbol('x')
expr = 0 - expressions.Sin(x)

def adjoint(tree):
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
    print(f"Adjoint: {tree}: {tree.adjoint}")
    for child in tree.operands:
        adjoint(child)

#evalpostvisitor(expr1, symbol_map={'x':2, 'y':1, 'a':1})
#previsitor(expr)
#adjoint(expr)

def childnodes(tree, nodes):
    if isinstance(tree, expressions.Symbol):
        nodes.append(tree)
    for child in tree.operands:
        childnodes(child, nodes)

x = expressions.Symbol('x')
y = expressions.Symbol('y')
a = expressions.Symbol('a')
conditions = {'x':2, 'y':1, 'a':2}
expression = x**3 + expressions.Sin(x) - 5

def reversemodeAD(expr, conditions):
    nodes = []
    childnodes(expr, nodes)
    evalpostvisitor(expr, symbol_map=conditions)
    previsitor(expr)
    symbols = dict()
    for node in nodes:
        symbols[node] = node.adjoint
    return symbols

print(reversemodeAD(expression, conditions))
