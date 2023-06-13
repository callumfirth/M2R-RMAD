from rmad.evaluate import evaluate, adjoint_evaluate
from rmad.expressions import Symbol
import numpy as np


def evalpostvisitor(expr, **kwargs):
    """
    Visit an expression in post-order applying a function.
    """
    stack = []
    if isinstance(expr, np.ndarray):
        for expression in expr:
            stack.append(expression)
    else:
        stack = [expr]
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
            visited[element] = evaluate(element,
                                        *(visited[operand] for operand in
                                          element.operands),
                                        **kwargs)
            element.storedvalue = visited[element]


def adjointprevisitor(expr, fn_adjoint=1, **kwargs):
    """
    Traverse tree in preorder applying the adjoint to each node.

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
    adjoint = adjoint_evaluate(expr, *(o.storedvalue for o in expr.operands))
    for counter, operand in enumerate(expr.operands):
        operand.adjoint += adjoint[counter] * expr.adjoint
        adjointprevisitor(operand, operand.adjoint)
        if not isinstance(operand, Symbol):
            operand.adjoint = 0  # So that next pass the adjoints are set to 0


def adjoint(tree):
    """Print adjoint values of all the nodes in the tree."""
    print(f"Value,adjoint: {tree}: {tree.storedvalue}, {tree.adjoint}")
    for child in tree.operands:
        adjoint(child)


def symbolnodes(tree, nodes):
    if isinstance(tree, Symbol):
        nodes.append(tree)
    for child in tree.operands:
        symbolnodes(child, nodes)
