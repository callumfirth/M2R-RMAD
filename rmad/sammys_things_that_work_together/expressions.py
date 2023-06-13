# """Module to represent mathematical expressions."""
# from numbers import Number as Num
# from functools import singledispatch


# class Expression:
#     """Main expression class."""

#     def __init__(self, *operands):
#         self.operands = operands

#     def __add__(self, other):
#         if isinstance(other, Num):
#             other = Number(other)
#         return Add(self, other)

#     def __radd__(self, other):
#         if isinstance(other, Num):
#             return Add(Number(other), self)

#     def __sub__(self, other):
#         if isinstance(other, Num):
#             other = Number(other)
#         return Sub(self, other)

#     def __rsub__(self, other):
#         if isinstance(other, Num):
#             return Sub(Number(other), self)  # I think this should have a minus infront

#     def __mul__(self, other):
#         if isinstance(other, Num):
#             other = Number(other)
#         return Mul(self, other)

#     def __rmul__(self, other):
#         if isinstance(other, Num):
#             return Mul(Number(other), self)

#     def __truediv__(self, other):
#         if isinstance(other, Num):
#             other = Number(other)
#         return Div(self, other)

#     def __rtruediv__(self, other):
#         if isinstance(other, Num):
#             return Div(Number(other), self)

#     def __pow__(self, other):
#         if isinstance(other, Num):
#             other = Number(other)
#         return Pow(self, other)

#     def __rpow__(self, other):
#         if isinstance(other, Num):
#             return Pow(Number(other), self)


# class Terminal(Expression):
#     """Symbols used in expression."""

#     precedence = 3

#     def __init__(self, value):
#         self.value = value
#         super().__init__()

#     def __repr__(self):
#         return repr(self.value)

#     def __str__(self):
#         return str(self.value)


# class Number(Terminal):
#     """Numbers used in the expression."""

#     def __init__(self, value):
#         if not isinstance(value, Num):
#             raise TypeError(
#                 f"Number value must be number not {type(value)}"
#             )
#         super().__init__(value)


# class Symbol(Terminal):
#     """Symbols used in the expression."""

#     def __init__(self, value):
#         if not isinstance(value, str):
#             raise TypeError(
#                 f"Symbol value must be string not {type(value)}"
#             )
#         super().__init__(value)


# class Operator(Expression):
#     """Operators used in the expression."""

#     def __repr__(self):
#         return type(self).__name__ + repr(self.operands)

#     def __str__(self):

#         def parenth(operand):
#             if operand.precedence < self.precedence:
#                 return f"({str(operand)})"
#             else:
#                 return str(operand)

#         return " ".join((parenth(self.operands[0]),
#                          self.symbol,
#                          parenth(self.operands[1])))


# class Add(Operator):
#     """Addition operator."""

#     symbol = "+"
#     precedence = 1


# class Mul(Operator):
#     """Multiplication operator."""

#     symbol = "*"
#     precedence = 2


# class Sub(Operator):
#     """Subtraction operator."""

#     symbol = "-"
#     precedence = 1


# class Div(Operator):
#     """Division operator."""

#     symbol = "/"
#     precedence = 2


# class Pow(Operator):
#     """Power operator."""

#     symbol = "^"
#     precedence = 3


# # x = Symbol("x")
# # y = Symbol("y")

# # expr = x + y**2

# # print(expr)

# # def fn(node, p):
# #     depth = p + 1 if p else 1
# #     print(f"{node}: {depth}")
# #     return depth


# # hi = previsitor(expr, fn)


# @singledispatch
# def differentiate(expr, *o, **kwargs):
#     """Differentiation implentation using postvisitor func."""
#     raise NotImplementedError


# @differentiate.register(Number)
# def _(expr, *o, **kwargs):
#     return 0.0


# @differentiate.register(Symbol)
# def _(expr, *o, **kwargs):
#     return 1.0 if kwargs['var'] == expr.value else 0.0


# @differentiate.register(Add)
# def _(expr, *o, **kwargs):
#     return o[0] + o[1]


# @differentiate.register(Sub)
# def _(expr, *o, **kwargs):
#     return o[0] - o[1]


# @differentiate.register(Mul)
# def _(expr, *o, **kwargs):
#     return o[0] * expr.operands[1] + o[1] * expr.operands[0]


# @differentiate.register(Div)
# def _(expr, *o, **kwargs):
#     return (o[0] * expr.operands[1] -
#             expr.operands[0] * o[1]) / (expr.operands[1] ** 2)


# @differentiate.register(Pow)
# def _(expr, *o, **kwargs):
#     return expr.operands[1] * (expr.operands[0] **
#                                (expr.operands[1] - 1)) * o[0]


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


def previsitor(expr, fn, fn_initial=None, **kwargs):
    visited = {expr: fn_initial}
    current_level_nodes = [expr]

    while current_level_nodes:
        new_level_nodes = []

        for node in current_level_nodes:
            for o in node.operands:
                visited[o] = fn(o, visited[node], **kwargs)
                new_level_nodes.append(o)

        current_level_nodes = new_level_nodes



"""Module to represent mathematical expressions."""
from numbers import Number as Num


class Expression:
    """Main expression class."""

    def __init__(self, *operands):
        self.operands = operands
        self.storedvalue = 0
        self.adjoint = 0

    def __add__(self, other):
        if isinstance(other, Num):
            other = Number(other)
        return Add(self, other)

    def __radd__(self, other):
        if isinstance(other, Num):
            return Add(Number(other), self)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Num):
            other = Number(other)
        return Sub(self, other)

    def __rsub__(self, other):
        if isinstance(other, Num):
            return Sub(Number(other), self)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Num):
            other = Number(other)
        return Mul(self, other)

    def __rmul__(self, other):
        if isinstance(other, Num):
            return Mul(Number(other), self)
        else:
            return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Num):
            other = Number(other)
        return Div(self, other)

    def __rtruediv__(self, other):
        if isinstance(other, Num):
            return Div(Number(other), self)
        else:
            return NotImplemented

    def __pow__(self, other):
        if isinstance(other, Num):
            other = Number(other)
        return Pow(self, other)

    def __rpow__(self, other):
        if isinstance(other, Num):
            return Pow(Number(other), self)
        else:
            return NotImplemented


class Terminal(Expression):
    """Symbols used in expression."""

    precedence = 5

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class Number(Terminal):
    """Numbers used in the expression."""

    def __init__(self, value):
        if not isinstance(value, Num):
            raise TypeError(
                f"Number value must be number not {type(value)}"
            )
        super().__init__(value)


class Symbol(Terminal):
    """Symbols used in the expression."""

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f"Symbol value must be string not {type(value)}"
            )
        super().__init__(value)


class Operator(Expression):
    """Operators used in the expression."""

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):

        def parenth(operand):
            if operand.precedence < self.precedence:
                return f"({str(operand)})"
            else:
                return str(operand)
        return " ".join((parenth(self.operands[0]),
                         self.symbol,
                         parenth(self.operands[1])))


class Function(Operator):

    def __repr__(self):
        return type(self).__name__ + "(" + repr(self.operands[0]) + ")"

    def __str__(self):
        return self.symbol + "(" + str(self.operands[0]) + ")"

    def __call__(self, value):
        return type(self)(value)

    precedence = 3


class Add(Operator):
    """Addition operator."""

    symbol = "+"
    precedence = 0


class Mul(Operator):
    """Multiplication operator."""

    symbol = "*"
    precedence = 1


class Sub(Operator):
    """Subtraction operator."""

    symbol = "-"
    precedence = 0


class Div(Operator):
    """Division operator."""

    symbol = "/"
    precedence = 1


class Pow(Operator):
    """Power operator."""

    symbol = "^"
    precedence = 4


class Sin(Function):
    """Sine function."""

    symbol = "sin"
    precedence = 3


class Cos(Function):
    """Cosine function."""

    symbol = "cos"
    precedence = 3


class Exp(Function):
    """Exponential function."""

    symbol = "exp"
    precedence = 4


class Log(Function):
    """Logarithmic function."""

    symbol = "log"
    precedence = 4