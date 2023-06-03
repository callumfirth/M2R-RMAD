from evaluate import evaluate, adjoint_evaluate
from expressions import Operator, Symbol, Function


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
            if isinstance(element, (Operator, Function)):
                element.adjoint = 0
    return visited[expr]


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
        operand.adjoint += adjoint_evaluate(expr,
                                            *(o.storedvalue for o in expr.operands))[counter] * expr.adjoint
        adjointprevisitor(operand, operand.adjoint)


def adjoint(tree):
    """Print adjoint values of all the nodes in the tree"""
    print(f"Adjoint: {tree}: {tree.adjoint}")
    for child in tree.operands:
        adjoint(child)


def symbolnodes(tree, nodes):
    if isinstance(tree, Symbol):
        nodes.append(tree)
    for child in tree.operands:
        symbolnodes(child, nodes)
