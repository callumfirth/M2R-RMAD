from rmad.evaluate import evaluate, adjoint_evaluate
from rmad.expressions import Symbol
import numpy as np


def evalpostvisitor(expr, **kwargs):
    """Visit an expression in post-order evaluating the operator"""
    # Below is used to make func non recursive
    stack = []
    # If we have multiple outputs push each subexpr to stack
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
            # The evaluate method below
            visited[element] = evaluate(element,
                                        *(visited[operand] for operand in
                                          element.operands),
                                        **kwargs)
            element.storedvalue = visited[element]


def adjointprevisitor(expr, fn_adjoint=1, **kwargs):
    """
    Traverse tree in preorder applying the adjoint to each node.

    Traverses the tree in preorder, where we visit the children after parent
    then recursively calls itself. Here we visit the parent node and
    then calculates the adjoint to give to each of its children using
    adjoint_evaluate method. Then loops through operands and adds
    the respective adjoint.

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
    adjoints = adjoint_evaluate(expr, *(o.storedvalue for o in expr.operands))
    for counter, operand in enumerate(expr.operands):
        operand.adjoint += adjoints[counter]
        adjointprevisitor(operand, operand.adjoint)
        if not isinstance(operand, Symbol):  # Useful if expr has >1 outputs
            operand.adjoint = 0  # So that next pass the adjoints are set to 0


def adjoint(tree):
    """
    Print adjoint values of all the nodes in the tree.

    Useful for testing and to see the adjoint at each expressions/operator.
    """
    print(f"Value,adjoint: {tree}: {tree.storedvalue}, {tree.adjoint}")
    for child in tree.operands:
        adjoint(child)


def symbolnodes(tree, nodes):  # Not currently used
    """Gets all the symbols in the tree."""
    if isinstance(tree, Symbol):
        nodes.append(tree)
    for child in tree.operands:
        symbolnodes(child, nodes)


def set0(tree):
    """
    Set adjoints and storedvalue to 0.

    Useful for testing and to see the adjoint at each expressions/operator.
    """
    tree.adjoint = 0
    tree.storedvalue = 0
    for child in tree.operands:
        set0(child)
