import graphviz as gv
from matplotlib.pyplot import xlabel
import numpy as np
import rmad.expressions as expressions


def exprpostvisitor(expr, graph, node="v", numsymbol=0, xlab=False, **kwargs):
    """Setup edges and nodes to be drawn as a DAG."""
    stack = []
    if isinstance(expr, np.ndarray):
        for expression in expr:
            stack.append(expression)
    else:
        stack = [expr]
    visited = {}
    id = 0 if not numsymbol else -numsymbol
    while stack:
        element = stack.pop()
        unvisited_children = []
        for operand in reversed(element.operands):
            if operand not in visited:
                unvisited_children.append(operand)
        if unvisited_children:
            stack.append(element)
            for x in unvisited_children:
                stack.append(x)
        else:
            id += 1
            if isinstance(element, (expressions.Number, expressions.Symbol)):
                name = element.value
            else:
                name = element.symbol
            if xlab:
                label = f'<{node}<SUB>{id}</SUB>>'
            else:
                label = ""
            graph.node(f'{node}_{id}', str(name), xlabel=label)

            visited[element] = f'{node}_{id}'
            for operand in element.operands:
                graph.edge(visited[element], visited[operand],
                           constraint='true', minlen='1.5')


def draw_expression(expr, name, xlab=False, numsymbol=0):
    """Draw expression as a DAG."""
    graph = gv.Digraph(engine='dot')
    exprpostvisitor(expr, graph, numsymbol=2, xlab=xlab)
    graph.attr(margin="0")
    graph.format = 'pdf'
    graph.render(f'images/Graph_{name}', view=True)


def draw_cluster(expr1, expr2, name, xlab=False, numsymbol=0):
    """Draw two expressions side by side."""
    graph = gv.Digraph(engine='dot')

    with graph.subgraph(name='cluster_DAG') as cluster1:
        cluster1.attr(label="Expression Tree")
        exprpostvisitor(expr1, cluster1, node="v")

    with graph.subgraph(name='cluster_Tree') as cluster2:
        cluster2.attr(label="Expression DAG")
        exprpostvisitor(expr2, cluster2, node="w")

    graph.attr(margin="0")
    graph.format = 'pdf'
    graph.render(f'images/Graph_{name}', view=True)
