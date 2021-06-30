"""This module provides the DiscreteTimeDomainSequence class to
represent discrete-time domain sequences.

Copyright 2021 Michael Hayes, UCECE

"""

from .domains import DiscreteTimeDomain
from .sequence import Sequence
from .dsym import nsym

__all__ = ('nseq', )

class DiscreteTimeDomainSequence(DiscreteTimeDomain, Sequence):
    """Discrete-time domain sequence."""

    var = nsym
    
    def DFT(self):
        """Calculate DFT and return as sequence."""

        from sympy import exp
        from .sym import j, pi
        from .kexpr import k

        results = []
        vals = self.vals
        N = len(vals)
        for ki in range(N):
            result = 0
            for ni in range(N):            
               result += vals[ni] * exp(-2 * j * pi * self.n[ni] * ki / N)
            results.append(result)

        from .kseq import DiscreteFourierDomainSequence
        return DiscreteFourierDomainSequence(results)

    def ZT(self):
        """Calculate z-transform and return as sequence."""

        from .zexpr import z

        results = []
        vals = self.vals
        N = len(vals)
        for ni in range(N):
            results.append(z**(-ni) * vals[ni].expr)

        from .zseq import ZDomainSequence                        
        return ZDomainSequence(results)        
    

def nseq(arg, ni=None, origin=None):
    """Create a discrete-time domain Sequence from a tuple, list, ndarray, or str.

    >>> a = nseq((1, 2, 3))

    The sequence indices are specified with the optional `ni` argument.
    For example:
    
    >>> a = nseq((1, 2, 3, 4), (-1, 0, 1, 2))

    If the `ni` argument is not specified, the sequence indices
    are enumerated from 0.

    With a string argument, an underscore indicates the zero sequence
    index:

    >>> a = nseq('{1, _2, 3, 4}')

    The sequence indices can be found using the `n` attribute.
    This returns a list.

    >>> a = nseq('{1, _2, 3, 4}').n
    [-1, 0, 1, 2]
    """    
    
    return DiscreteTimeDomainSequence(arg, ni, origin)