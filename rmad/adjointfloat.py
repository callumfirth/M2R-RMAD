import math


class AdjointFloat(float):

    def __init__(self, value=None, adjoint=0):
        self.value = value
        self.adjoint = adjoint

    def __neg__(self):
        return AdjointFloat(value=-self.value, adjoint=-self.adjoint)

    def __add__(self, u):
        v = AdjointFloat(self.value + u.value)
        v.adjoint = tuple((self, u))
        return v

    def __sub__(self, u):
        v = AdjointFloat(self.value - u.value)
        v.adjoint = tuple((self, -u))
        return v

    def sin(u):
        v = AdjointFloat(math.sin(u.value))
        v.adjoint = math.cos(u.value)*u.adjoint
        return v

    def cos(u):
        v = AdjointFloat(math.cos(u.value))
        v.adjoint = -math.sin(u.value)*u.adjoint
        return v

    def exp(u):
        v = AdjointFloat(math.exp(u.value))
        v.adjoint = math.exp(u.value)*u.adjoint
        return v

    def log(u):
        v = AdjointFloat(math.log(u.value))
        v.adjoint = (1/u.value)*u.adjoint
        return v
