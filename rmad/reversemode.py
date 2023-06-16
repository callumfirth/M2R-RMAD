from rmad.traversal import evalpostvisitor, adjointprevisitor
import numpy as np


def reversemodeAD(expr, conditions):
    """Return dict of the derivatives of expr w.r.t symbols."""
    # First forward traverse the graph
    evalpostvisitor(expr, symbol_map=conditions)

    # Now do the reverse pass
    if isinstance(expr, np.ndarray):  # If we have multiple outputs

        symbols = dict((symbol, []) for symbol in conditions)
        for expression in expr:

            # If output of our value is nparray
            if isinstance(expr.storedvalue, np.ndarray):
                adjoint = np.ones(len(expr.storedvalue))
            else:
                adjoint = 1

            # Backward traverse the tree (previsitor)
            adjointprevisitor(expression, fn_adjoint=adjoint)
            for symbol in conditions.keys():
                symbols[symbol].append(symbol.adjoint)  # Store adjoint values
                symbol.adjoint = 0  # So next pass, adjoints are set back to 0

    else:  # If we have only 1 output, i.e. m=1
        # Backward traverse the tree

        #If output of our value is nparray
        if isinstance(expr.storedvalue, np.ndarray):
            adjoint = np.ones(len(expr.storedvalue))
        else:
            adjoint = 1

        adjointprevisitor(expr, fn_adjoint=adjoint)
        # For each symbol, return the dict of the repsective adjoint
        symbols = dict((symbol, symbol.adjoint) for symbol in conditions)
    return symbols
