from visitor import postvisitor, previsitor
from evaluate import evaluate, _closeto0
import expressions
from functools import singledispatchmethod

class ReverseMode:
    def __init__(self, expr, symbol_map):
        self.expr = expr
        self.symbol_map = symbol_map

        self.node_av_pairs = {}

    def forward_pass(self):
        node_value_dict = postvisitor(self.expr, evaluate, symbol_map=self.symbol_map)

        for node in node_value_dict.items():
            self.node_av_pairs[node[0]] = [node[1], None]

    def reverse_pass(self):
        self.node_av_pairs[self.expr][1] = 1
        previsitor(self.expr, self.set_child_adjoint_values)

        return self.node_av_pairs
    
    def compute_derivatives(self):
        self.forward_pass()

        return self.reverse_pass()

    def set_child_adjoint_values(self, expr):
        if self.node_av_pairs[expr][1] is None:
            adjoints = self.reverse_evaluate(expr) * self.node_av_pairs[expr][1]

            self.node_av_pairs |= dict((e, a) for e, a in zip(expr.operands, adjoints))

    @singledispatchmethod
    def reverse_evaluate(self, expr, *cv):
        raise NotImplementedError(f"Cannot evaluate a {type(expr).__name__}")
    
    @reverse_evaluate.register(expressions.Number)
    def _(self, expr):
        return [float("NaN")]

    @reverse_evaluate.register(expressions.Symbol)
    def _(self, expr):
        return [float("NaN")]

    @reverse_evaluate.register(expressions.Add)
    def _(self, expr):
        return np.array([1, 1])

    @reverse_evaluate.register(expressions.Sub)
    def _(self, expr):
        return np.array([1, -1])


    @reverse_evaluate.register(expressions.Mul)
    def _(self, expr, *cv):
        return np.array([cv[1], cv[0]])


    @reverse_evaluate.register(expressions.Div)
    def _(self, expr):
        return np.array([1/(cv[1]), -cv[0]/(cv[1]**2)])


    @reverse_evaluate.register(expressions.Pow)
    def _(self, expr, *cv):
        return np.array([cv[0]**cv[1] * np.log(cv[0], cv[1] * cv[0]**(cv[1]-1))])  # This is the other way around to callum's


    @reverse_evaluate.register(expressions.Sin)
    def _(self, expr, *cv):
        return np.array([_closeto0(np.cos(o[0]))])

    @reverse_evaluate.register(expressions.Cos)
    def _(self, expr, *cv):
        return np.array([_closeto0(-np.sin(cv[0]))])


    @reverse_evaluate.register(expressions.Exp)
    def _(self, expr, *cv):
        return np.array([np.exp(cv[0])])


    @reverse_evaluate.register(expressions.Log)
    def _(self, expr, *cv):
        return np.array([1/(cv[0])])






x = expressions.Symbol("x")
y = expressions.Symbol("y")

expr = x * expressions.Sin(x+y)

hi = ReverseMode(expr, {"x": 1, "y": 1}).compute_derivatives()

print(hi)