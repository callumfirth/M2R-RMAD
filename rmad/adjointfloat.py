import math


class AdjointFloat(float):

    def __init__(self, value=None, adjoint=0):
        self.value = value
        self.partialderivatives = adjoint

    def __add__(self, u):
        v = AdjointFloat(self.value + u.value)
        v.adjoint = tuple([(self, 1), (u, 1)])
        return v

    def __sub__(self, u):
        v = AdjointFloat(self.value - u.value)
        v.adjoint = tuple([(self, 1), (u, -1)])
        return v
    
    def __mul__(self, u):
        v = AdjointFloat(self.value - u.value)
        v.adjoint = tuple([(self, u.value), (u, self.value)])
        return v
    
    def __truediv__(self, u):
        v = AdjointFloat(self.value - u.value)
        v.adjoint = tuple([(self, 1/u.value), (u, -1*self.value/u.value**2)])
        return v
    
    def __pow__(self, u):
        v = AdjointFloat(self.value - u.value)
        v.adjoint = tuple((self, -u))
        return v
    
    def __neg__(self):
        v = AdjointFloat(-self.value)
        v.adjoint = tuple((self, -1))
        return v

    def sin(u):
        v = AdjointFloat(math.sin(u.value))
        v.adjoint = tuple(u,math.cos(u.value)*u.adjoint)
        return v

    def cos(u):
        v = AdjointFloat(math.cos(u.value))
        v.adjoint = tuple(u,-math.sin(u.value)*u.adjoint)
        return v

    def exp(u):
        v = AdjointFloat(math.exp(u.value))
        v.adjoint = tuple(u,math.exp(u.value)*u.adjoint)
        return v

    def log(u):
        v = AdjointFloat(math.log(u.value))
        v.adjoint = tuple(u,(1/u.value)*u.adjoint)
        return v
    

def postvisitor(expr, fn, **kwargs):
    """Visit an expression in post-order applying a function."""
    stack = [expr]
    visited = {}
    while stack:
        element = stack.pop()
        unvisited_children = []
        for operand in element.operands:
            if operand not in visited:
                unvisited_children.append(operand)
        if unvisited_children:
            stack.append(element)
            for x in unvisited_children:
                stack.append(x)
        else:  # Need to modify this to stores tuple? with val and adjoint
            visited[element] = fn(element,
                            *(visited[operand] for operand in element.operands),
                            **kwargs)
    return visited[expr]


#Say we have expression Sin(x+y)*Cos(x+y)+exp(x)
#Then we have Add(Exp(x), Mul(Sin(Add(x, y)), Cos(Add(x, y))))
#With out top node being Add( . . . )
#And "child" nodes being Add(x, y) and Exp(x)

#Postvisitor func allows us to traverse this forwards (child to parent)
#A previsitor func allows us to traverse this backwards (parent to child)
#Then we want to traverse "backwards"
