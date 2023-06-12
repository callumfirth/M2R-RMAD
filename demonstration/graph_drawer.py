import graphviz as gv
import numpy as np
import rmad.expressions as expressions

def exprpostvisitor(expr, graph, **kwargs):
    """Visit an expression in post-order applying a function."""
    stack = []
    if isinstance(expr, np.ndarray):
        for expression in expr:
            stack.append(expression)
    else:
        stack = [expr]
    visited = {}
    id = 0
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
            id += 1
            if isinstance(element, expressions.Number):
                name = element.value
            elif isinstance(element, expressions.Symbol):
                name = element.value
            else:
                name = element.symbol
            graph.node(f'v_{id}', str(name))
            visited[element] = f'v_{id}'
            for operand in element.operands:
                graph.edge(visited[element], visited[operand],
                           constraint='true', minlen='1.5')


def draw_expression(expr, name):

    graph = gv.Digraph(engine='dot')

    exprpostvisitor(expr, graph)

    graph.attr(margin="0")
    graph.format = 'pdf'
    graph.render(f'images/Graph_{name}', view=True)
