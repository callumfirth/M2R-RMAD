from rmad.traversal import evalpostvisitor, adjointprevisitor
import numpy as np


def reversemodeAD(expr, conditions):
    """Return dict of the derivatives of expr w.r.t symbols."""
    try:
        evalpostvisitor(expr, symbol_map=conditions)  # Forward traverse
    except ZeroDivisionError:  # Not currently used i dont think
        raise Exception("Function not valid at initial condition")


    if isinstance(expr, np.ndarray):
        if isinstance(expr[0].storedvalue, (np.ndarray, list)):
            adjoint = np.ones(len(expr[0].storedvalue))
        else:
            adjoint = 1
        symbols = dict((symbol, []) for symbol in conditions)
        for expression in expr:
            adjointprevisitor(expression, fn_adjoint=adjoint)  # Backwards traverse the tree
            for symbol in conditions.keys():
                symbols[symbol].append(symbol.adjoint)  # Store adjoint values
                symbol.adjoint = 0  # So next pass, adjoints are set back to 0
    else:
        if isinstance(expr.storedvalue, (np.ndarray, list)):
            adjoint = np.ones(len(expr.storedvalue))
        else:
            adjoint = 1
        adjointprevisitor(expr, fn_adjoint=adjoint)  # Backwards traverse through the tree
        # For each symbol, return the dict of the repsective adjoint
        symbols = dict((symbol, symbol.adjoint) for symbol in conditions)
    return symbols
