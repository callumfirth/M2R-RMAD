from visitors import postvisitor
from evaluate import evaluate, _closeto0
import expressions
from functools import singledispatchmethod
import numpy as np


class ReverseMode:
    """Implementation of Reverse-Mode Algorithmic Differentiation."""

    def __init__(self, expr, symbol_map):
        """Initialise R-M AD."""
        self.expr = expr
        self.symbol_map = symbol_map

        self.node_av_pairs = {}

    def forward_pass(self):
        """Perform the forward pass appling the postvisitor function."""
        node_value_dict = postvisitor(self.expr, evaluate, symbol_map=self.symbol_map)

        for node in node_value_dict.items():
            self.node_av_pairs[node[0]] = [node[1], None]

    def reverse_pass(self):
        """Perform the reverse pass appling the previsitor function."""
        self.node_av_pairs[self.expr][1] = 1
        self.previsitor(self.expr, self.set_child_adjoint_values)

        return self.node_av_pairs

    def compute_partial_derivatives(self):
        """Calculate the av pairs."""
        self.forward_pass()
        self.reverse_pass()

        p_d = {node: self.node_av_pairs[node][1] for node in self.node_av_pairs if type(node) == expressions.Symbol}

        return p_d

    def set_child_adjoint_values(self, expr):
        """Set the ajoint values of the children of a node."""
        child_values = [self.node_av_pairs[c][0] for c in expr.operands]
        adjoints = self.reverse_evaluate(expr, *child_values) * self.node_av_pairs[expr][1]

        for i, o in enumerate(expr.operands):
            if type(o) == expressions.Symbol:
                try:
                    self.node_av_pairs[o][1] += adjoints[i]
                except TypeError:
                    self.node_av_pairs[o][1] = adjoints[i]
            else:
                self.node_av_pairs[o][1] = adjoints[i]

    @singledispatchmethod
    def reverse_evaluate(self, expr, *cv):
        """Calculate the partial derivatives of the parent with respect to the children."""
        raise NotImplementedError(f"Cannot evaluate a {type(expr).__name__}")

    @reverse_evaluate.register(expressions.Number)
    def _(self, expr, *cv):
        return np.array([0])

    @reverse_evaluate.register(expressions.Symbol)
    def _(self, expr, *cv):
        return np.array([0])

    @reverse_evaluate.register(expressions.Add)
    def _(self, expr, *cv):
        return np.array([1, 1])

    @reverse_evaluate.register(expressions.Sub)
    def _(self, expr, *cv):
        return np.array([1, -1])

    @reverse_evaluate.register(expressions.Mul)
    def _(self, expr, *cv):
        return np.array([cv[1], cv[0]])

    @reverse_evaluate.register(expressions.Div)
    def _(self, expr, *cv):
        return np.array([1/(cv[1]), -cv[0]/(cv[1]**2)])

    @reverse_evaluate.register(expressions.Pow)
    def _(self, expr, *cv):
        return np.array([ cv[1] * cv[0]**(cv[1]-1), cv[0]**cv[1] * np.log(cv[0])])

    @reverse_evaluate.register(expressions.Sin)
    def _(self, expr, *cv):
        return np.array([_closeto0(np.cos(cv[0]))])

    @reverse_evaluate.register(expressions.Cos)
    def _(self, expr, *cv):
        return np.array([_closeto0(-np.sin(cv[0]))])

    @reverse_evaluate.register(expressions.Exp)
    def _(self, expr, *cv):
        return np.array([np.exp(cv[0])])

    @reverse_evaluate.register(expressions.Log)
    def _(self, expr, *cv):
        return np.array([1/(cv[0])])

    def previsitor(self, expr, fn):
        """Visit an expression in pre-order applying a function."""
        current_level_nodes = [expr]

        while current_level_nodes:
            new_level_nodes = []

            for node in current_level_nodes:
                fn(node)

                for o in node.operands:
                    new_level_nodes.append(o)

            current_level_nodes = new_level_nodes


x = expressions.Symbol("x")
y = expressions.Symbol("y")

expr = 2*x*(y/2)**2
reverse = ReverseMode(expr, {"x": 10, "y": 1})
partial_derivatives = reverse.compute_partial_derivatives()

print(partial_derivatives)
