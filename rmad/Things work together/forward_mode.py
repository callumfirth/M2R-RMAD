import expressions
from evaluate import evaluate, _closeto0
from functools import singledispatch
import numpy as np


# def forward_mode(expr, conditions):
#     return 

@singledispatch
def forward_evaluate(expr, *o, **kwargs):
    raise NotImplementedError(f"Cannot evaluate a {type(expr).__name__}")

@forward_evaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    return [evaluate(expr), 0]

@forward_evaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, seed, **kwargs):
    if seed[expr.value] == symbol_map[expr.value]:
        return [evaluate(expr, symbol_map=symbol_map), 1]

    return [evaluate(expr, symbol_map=symbol_map), 0]


@forward_evaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), o[0][1] + o[1][1]]


@forward_evaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), o[0][1] - o[1][1]]


@forward_evaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), o[1][0] * o[0][1] + o[0][0] * o[1][1]]


@forward_evaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), 1/o[1][0] * o[0][1] - (o[0][0]/(o[1][0]**2)) * o[1][1]]


@forward_evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), (o[1][0] * o[0][0]**(o[1][0]-1)) * o[0][1] + (o[0][0]**o[1][0] * np.log(o[0][0])) * o[1][1]]


@forward_evaluate.register(expressions.Sin)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), _closeto0(np.cos(o[0][0])) * o[0][1]]

@forward_evaluate.register(expressions.Cos)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), _closeto0(-np.sin(o[0][0])) * o[0][1]]


@forward_evaluate.register(expressions.Exp)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), np.exp(o[0][0]) * o[0][1]]


@forward_evaluate.register(expressions.Log)
def _(expr, *o, **kwargs):
    return [evaluate(expr, *list(zip(*o))[0]), (1/o[0][o]) * o[0][1]]



x = expressions.Symbol("x")
y = expressions.Symbol("y")

expr = expressions.Sin(x + y) * x

print(expressions.postvisitor(expr, forward_evaluate, symbol_map={"x": 1, "y": 1}, seed={"x": 0, "y": 1}))
