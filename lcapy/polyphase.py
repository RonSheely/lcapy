"""This module provides preliminary support for polyphase systems. 

Copyright 2020 Michael Hayes, UCECE

"""

from .matrix import Matrix
from .sym import j, pi
from .functions import exp
from .expr import expr
from .phasor import Vphasor, Iphasor
from .vector import Vector


class PolyphaseVector(Vector):
    pass


class PolyphaseVoltageVector(PolyphaseVector):
    pass


class PolyphaseCurrentVector(PolyphaseVector):
    pass


class PhaseVoltageVector(PolyphaseVoltageVector):
    """These are the phase voltages with respect to a system ground."""

    def sequence(self):
        """Convert to sequence voltage vector."""
        A = polyphase_decompose_matrix(len(self))
        return SequenceVoltageVector(A * self)

    def line(self):
        """Convert to line voltage vector."""        
        D = phase_to_line_matrix(len(self))
        return LineVoltageVector(D * self)

    
class PhaseCurrentVector(PolyphaseCurrentVector):
    """These are the phase currents."""    

    def sequence(self):
        """Convert to sequence current vector."""
        A = polyphase_decompose_matrix(len(self))
        return SequenceCurrentVector(A * self)        

    def line(self):
        """Convert to line current vector."""
        D = phase_to_line_matrix(len(self))
        return LineCurrentVector(D * self)
    

class SequenceVoltageVector(PolyphaseVoltageVector):

    def phase(self):
        """Convert to phase current vector."""

        A = polyphase_compose_matrix(len(self))
        return PhaseVoltageVector(A * self)

    def line(self):
        """Convert to line voltage vector."""        
        return self.phase().line()

    @property    
    def V0(self):
        """Zero sequence voltage component"""
        return self[0]

    @property    
    def V1(self):
        """Positive sequence voltage component"""
        return self[1]

    @property    
    def V2(self):
        """Negative sequence voltage component"""
        return self[2]    

    
class SequenceCurrentVector(PolyphaseCurrentVector):

    def phase(self):
        A = polyphase_compose_matrix(len(self))
        return PhaseCurrentVector(A * self)

    def line(self):
        """Convert to line current vector."""        
        return self.phase().line()

    @property    
    def I0(self):
        """Zero sequence current component"""
        return self[0]

    @property    
    def I1(self):
        """Positive sequence current component"""
        return self[1]

    @property    
    def I2(self):
        """Negative sequence current component"""
        return self[2]        

    
class LineVoltageVector(PolyphaseVoltageVector):
    """These are also known as phase to phase voltages."""

    @property    
    def Vab(self):
        return self[0]

    @property    
    def Vbc(self):
        return self[1]

    @property    
    def Vca(self):
        return self[2]


class LineCurrentVector(PolyphaseCurrentVector):
    """These are also known as phase to phase currents."""
    pass


def phase_to_line_matrix(N=3):

    a = Matrix.zeros(N)
    
    for row in range(N):
        a[row, row] = 1
        col = (row + 1) % N
        a[row, col] = -1
    return a


def polyphase_decompose_matrix(N=3, expand=False):
    """Matrix to decompose vector of phase components into the symmetrical
    sequence components.  The matrix dimension is `N` x `N`.  This
    matrix is equivalent to IDFTmatrix.  The transformation is only
    valid for positive frequency components; the complex conjugate is
    required for negative frequency components.

    """
    
    if expand:
        alpha = polyphase_alpha(N)
    else:
        alpha = expr('alpha')

    a = Matrix.zeros(N)
    
    for row in range(N):
        for col in range(N):
            a[row, col] = alpha ** ((row * col) % N)
    return a


def polyphase_compose_matrix(N=3, expand=False):
    """Matrix to compose symmetrical sequence components into a vector of
    phase components.  The matrix dimension is `N` x `N`.  This matrix
    is equivalent to DFTmatrix.  The transformation is only valid for
    positive frequency components; the complex conjugate is required
    for negative frequency components.

    """

    if expand:
        alpha = polyphase_alpha(N)
    else:
        alpha = expr('alpha')

    a = Matrix.zeros(N)
    
    for row in range(N):
        for col in range(N):
            a[row, col] = alpha ** ((-row * col) % N)
    return a


def polyphase_alpha(N):

    return exp(-j * 2 * pi / N)


class PolyphaseVoltageCurrentVector(PolyphaseVector):
    """This is a stacked vector of voltages and currents."""

    @property
    def N_phases(self):
        return self.shape[0] // 2

    @property
    def N(self):
        return self.N_phases
    
    
class LineVoltageCurrentVector(PolyphaseVoltageCurrentVector):
    """These are also known as phase to phase voltages/currents."""

    @property
    def V(self):
        N = self.N_phases
        return LineVoltageVector(self[0:N])

    @property
    def I(self):
        N = self.N_phases
        return LineCurrentVector(self[N:])    

    @property    
    def Vab(self):
        return self.V[0]

    @property    
    def Vbc(self):
        return self.V[1]

    @property    
    def Vca(self):
        return self.V[2]
    

class PhaseVoltageCurrentVector(PolyphaseVoltageCurrentVector):
    
    @property
    def V(self):
        N = self.N_phases
        return PhaseVoltageVector(self[0:N])

    @property
    def I(self):
        N = self.N_phases
        return PhaseCurrentVector(self[N:])    

    def sequence(self):
        """Convert to sequence voltageCurrent vector."""

        A = polyphase_decompose_matrix(self.N)
        return SequenceVoltageCurrentVector(self.vstack(A * self.V, A * self.I))

    def line(self):
        """Convert to line voltageCurrent vector."""        
        D = phase_to_line_matrix(self.N)

        return LineVoltageCurrentVector((self.vstack(D * self.V, D * self.I)))

    @property    
    def Va(self):
        return self.V[0]

    @property    
    def Vb(self):
        return self.V[1]

    @property    
    def Vc(self):
        return self.V[2]

    @property    
    def Ia(self):
        return self.I[0]

    @property    
    def Ib(self):
        return self.I[1]

    @property    
    def Ic(self):
        return self.I[2]    


class SequenceVoltageCurrentVector(PolyphaseVoltageCurrentVector):

    @property
    def V(self):
        N = self.N_phases
        return SequenceVoltageVector(self[0:N])

    @property
    def I(self):
        N = self.N_phases
        return SequenceCurrentVector(self[N:])    
    
    def phase(self):
        """Convert to phase voltageCurrent vector."""

        A = polyphase_compose_matrix(self.N)
        
        return PhaseVoltageCurrentVector((self.vstack(A * self.V, A * self.I)))

    def line(self):
        """Convert to line voltageCurrent vector."""        
        return LineVoltageCurrentVector(self.vstack(self.V.line(), self.I.line()))
                                     
    @property    
    def V0(self):
        """Zero sequence voltage component"""
        return self.V[0]

    @property    
    def V1(self):
        """Positive sequence voltage component"""
        return self.V[1]

    @property    
    def V2(self):
        """Negative sequence voltage component"""
        return self.V[2]

    @property    
    def I0(self):
        """Zero sequence current component"""
        return self.I[0]

    @property    
    def I1(self):
        """Positive sequence current component"""
        return self.I[1]

    @property    
    def I2(self):
        """Negative sequence current component"""
        return self.I[2]    

                                     
