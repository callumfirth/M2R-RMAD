def previsitor(expr, fn, **kwargs):
    visited = {expr: None}
    current_level_nodes = [expr]
    leaf_values = {}

    while current_level_nodes:
        new_level_nodes = []

        for node in current_level_nodes:
            if not node.operands:
                leaf_values[node] = visited[node]
            else:
                for o in node.operands:
                    visited[o] = fn(o, visited[node], **kwargs)
                    new_level_nodes.append(o)

        current_level_nodes = new_level_nodes

    return leaf_values


x = Symbol("x")
y = Symbol("y")

expr = x**2 + x*y + y**3

print(expr)

def fn(node, p):
    depth = p + 1 if p else 1
    print(f"{node}: {depth}")
    return depth


hi = previsitor(expr, fn)
print(hi)