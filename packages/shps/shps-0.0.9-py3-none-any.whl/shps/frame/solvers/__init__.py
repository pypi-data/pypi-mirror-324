from .torsion import TorsionAnalysis
import numpy as np
class FlexureAnalysis:
    pass

class PlaneModel:
    def __init__(self, nodes, elems, offset=None):
        self.nodes = nodes 
        self.elems = elems
        self.offset = offset

    def cells(self):
        return [
            elem.nodes for elem in self.elems
        ]

    def translate(self, offset):
        return type(self)(self.nodes-offset, self.elems, self.offset)

class TriangleModel(PlaneModel):

    def rotate(self, angle):
        # TODO: Implement rotation of model
        return TriangleModel()

    def cell_area(self, tag=None)->float:
        if tag is None:
            return sum(self.cell_area(i) for i in range(len(self.elems)))

        y, z = self.nodes[self.elems[tag].nodes].T
        z1, z2, z3 = z
        y1, y2, y3 = y
        return -float(0.5 * ((y2 - y1) * (z3 - z1) - (y3 - y1) * (z2 - z1)))

    def cell_solution(self, tag, state):
        return float(sum(state[self.elems[tag].nodes]))/3

    def cell_gradient(self, tag, state):
        u1, u2, u3 = state[self.elems[tag].nodes]
        ((y1, y2, y3), (z1, z2, z3)) = self.nodes[self.elems[tag].nodes].T
        z12 = z1 - z2
        z23 = z2 - z3
        z31 = z3 - z1
        y32 = y3 - y2
        y13 = y1 - y3
        y21 = y2 - y1
        A = self.cell_area(tag)
        return 1/(2*A)*np.array([
            z23*u1 + z31*u2 + z12*u3,
            y32*u1 + y13*u2 + y21*u3
        ])

    def energy(self, u, v):
        q = 0.0
        for elem in self.elems:
            ((y1, y2, y3), (z1, z2, z3)) = self.nodes[elem.nodes].T

            z12 = z1 - z2
            z23 = z2 - z3
            z31 = z3 - z1
            y32 = y3 - y2
            y13 = y1 - y3
            y21 = y2 - y1

            area = -0.5 * ((y2 - y1) * (z3 - z1) - (y3 - y1) * (z2 - z1))

            k11 = ( y32**2 +  z23**2)
            k12 = (y13*y32 + z23*z31)
            k13 = (y21*y32 + z12*z23)
            k22 = ( y13**2 +  z31**2)
            k23 = (y13*y21 + z12*z31)
            k33 = ( y21**2 +  z12**2)

            ke = 1/(4.0*area)*np.array([[k11, k12, k13],
                                        [k12, k22, k23],
                                        [k13, k23, k33]])
            ue = u[elem.nodes]
            ve = v[elem.nodes]
            q += ue.dot(ke@ve)

        return q


    def inner(self, u, v):
        pass

    def curl(self, u, v):

        q = 0
        for elem in self.elems:
            ((y1, y2, y3), (z1, z2, z3)) = self.nodes[elem.nodes].T
            z12 = z1 - z2
            z23 = z2 - z3
            z31 = z3 - z1
            y32 = y3 - y2
            y13 = y1 - y3
            y21 = y2 - y1

            ((y1, y2, y3), (z1, z2, z3)) = u[elem.nodes].T

            f = 1/6.*np.array([
                ((y1*y32 - z1*z23) + (y2*y32 - z2*z23) + (y3*y32 - z3*z23)),
                ((y1*y13 - z1*z31) + (y2*y13 - z2*z31) + (y3*y13 - z3*z31)),
                ((y1*y21 - z1*z12) + (y2*y21 - z2*z12) + (y3*y21 - z3*z12))])
            
            q += f.dot(v[elem.nodes])

        return q
                 
    def inertia(self, va, ua):
        """
        v.dot( ([\int N.T rho @ N dA] @u)
        """
        q = 0.0
        for i,elem in enumerate(self.elems):
            v1, v2, v3 = va[elem.nodes]
            u1, u2, u3 = ua[elem.nodes]
            area = self.cell_area(i)
            # v[nodes].dot(int(N.T@N)@u[nodes])
            q += area/12.0*(u1*(2*v1+v2+v3) + u2*(v1+2*v2+v3) + u3*(v1+v2+2*v3))

        return float(q)

# ------------------------------------------------------------------------
# The following Python code is implemented by Professor Terje Haukaas at
# the University of British Columbia in Vancouver, Canada. It is made
# freely available online at terje.civil.ubc.ca together with notes,
# examples, and additional Python code. Please be cautious when using
# this code; it may contain bugs and comes without warranty of any form.
# ------------------------------------------------------------------------
# https://gist.githubusercontent.com/terjehaukaas/f633c4afc001badb4473d422ccc146e7/raw/2e7d09dbc850dc800c60e1751fb21f2f76615509/SolidCrossSectionAnalysis.py
# https://civil-terje.sites.olt.ubc.ca/files/2020/02/Screenshot-Solid-Cross-section.pdf
#