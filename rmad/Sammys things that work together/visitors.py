def previsitor(expr, fn, fn_initial=None, **kwargs):
    """Visit an expression in pre-order applying a function."""

    visited = {expr: fn_initial}
    current_level_nodes = [expr]

    while current_level_nodes:
        new_level_nodes = []

        for node in current_level_nodes:
            for o in node.operands:
                visited[o] = fn(o, visited[node], **kwargs)
                new_level_nodes.append(o)

        current_level_nodes = new_level_nodes


def postvisitor(expr, fn, **kwargs):
    """Visit an expression in post-order applying a function."""
    stack = [expr]
    visited = {}

    while stack:
        e = stack.pop()
        unvisited_children = []

        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)
            for x in unvisited_children:
                stack.append(x)
        else:
            visited[e] = fn(e,
                            *(visited[o] for o in e.operands),
                            **kwargs)
    return visited[expr]


# x = Symbol("x")
# y = Symbol("y")

# expr = x**2 + x*y + y**3

# print(expr)

# def fn(node, p):
#     depth = p + 1 if p else 1
#     print(f"{node}: {depth}")
#     return depth


# hi = previsitor(expr, fn)
# print(hi)