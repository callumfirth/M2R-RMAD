import networkx as nx
from expressions import *
import matplotlib.pyplot as plt
from previsitor import previsitor

x = Symbol("x")
y = Symbol("y")
z = Symbol("z")

expr = x*y/2 + y**2

### This relies on my previsitor function


class ExpressionGraph:  # There is a way to convert an nx graph to latex
    def __init__(self, expr):
        self.graph = nx.DiGraph()
        initial_id = (str(expr), 1)
        self.graph.add_node(initial_id)

        previsitor(expr, self.add_expression_node, fn_initial=initial_id)

    def add_expression_node(self, node, parent):
        if parent is not None:
            self.graph.add_edge(parent, (str(node), self.graph.number_of_nodes()))

        return str(node), self.graph.number_of_nodes()-1

    def display_graph(self):
        labels = {n: n[0] for n in self.graph.nodes()}

        for layer, nodes in enumerate(reversed(tuple(nx.topological_generations(self.graph)))):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer

        # Compute the multipartite_layout using the "layer" node attribute
        pos = nx.multipartite_layout(self.graph, subset_key="layer", align='horizontal')

        fig, ax = plt.subplots()
        nx.draw_networkx(self.graph, pos=pos, labels=labels,
                         node_color="White", bbox=dict(facecolor="skyblue",
                                                       boxstyle="round",
                                                       ec="silver", pad=0.3))
        fig.tight_layout()
        plt.show()

graph = ExpressionGraph(expr)

print(graph.graph.nodes)
print(graph.graph)

graph.display_graph()