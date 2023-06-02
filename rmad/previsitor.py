def previsitor(expr, fn, **kwargs):
    visited = {expr: None}
    current_level_nodes = [expr]

    while current_level_nodes:
        new_level_nodes = []

        for node in current_level_nodes:
            for o in node.operands:
                visited[o] = fn(o, visited[node], **kwargs)
                new_level_nodes.append(o)

        current_level_nodes = new_level_nodes

x = Symbol("x")
y = Symbol("y")

expr = x**2 + x*y + y**3

print(expr)

def fn(node, p):
    depth = p + 1 if p else 1
    print(f"{node}: {depth}")
    return depth


hi = previsitor(expr, fn)
