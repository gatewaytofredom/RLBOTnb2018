from vector3 import Vector3
import math


f = open("spl.csv", "w")

'''
Container for generalized hermite spline
'''
class HermiteSpline:
    def __init__(self, p0, p1, v0, v1):
        self.p0 = p0
        self.p1 = p1
        self.v0 = v0
        self.v1 = v1

    def get(self, t, scale):
        t = float(scale * t)

        x_basis = self.p1 - self.p0
        y_basis = x_basis.length() * Vector3.cross(x_basis, Vector3.k()).normalize()
        basis = Mat2x2.fromvectors(
            x_basis, 
            y_basis
        )

        print("MAT: {}".format(basis))

        transformed_v0 = (basis * self.v0).normalize()
        transformed_v1 = (basis * self.v1).normalize()

        slope_0 = transformed_v0.y / transformed_v0.x
        slope_1 = transformed_v1.y / transformed_v1.x

        print("SLOPES: {}, {}".format(slope_0, slope_1))

        spline =  Vector3(
            t,
            (self.H2(t) * slope_0) + (self.H3(t) * slope_1)
        )

        # print("SPLINE: {}".format(spline))
        f.write("{},{}\n".format(
            spline.x, spline.y 
        ))

        spline_der = Vector3(
            scale,
            (self.d_H2(t) * slope_0) + (self.d_H3(t) * slope_1)
        )

        #transform back to standard coords
        # inverse = basis.inverse()
        # if inverse == None:
        #     print("NO INVERSE: {}".format(basis))
        #     return Vector3.zero()

        return ((basis * spline) + self.p0, (basis * spline_der))

    #Hermite basis functions
    #https://www.rose-hulman.edu/~finn/CCLI/Notes/day09.pdf
    def H1(self, t):
        return 1 - (3 * math.pow(t, 2)) + (2 * math.pow(t, 3))
    
    def H2(self, t):
        return t - (2 * math.pow(t, 2)) + math.pow(t, 3)
    
    def H3(self, t):
        return -math.pow(t, 2) + math.pow(t, 3)
    
    def H4(self, t):
        return (3 * math.pow(t, 2)) - (2 * math.pow(t, 3))

    #Derivative functions
    def d_H1(self, t):
        return (-6 * t) + (6 * math.pow(t, 2))
    
    def d_H2(self, t):
        return 1 - (4 * t) + (3 * math.pow(t, 2))

    def d_H3(self, t):
        return (-2 * t) + (3 * math.pow(t, 2))

    def d_H4(self, t):
        return (6 * t) - (6 * math.pow(t, 2))

class Mat2x2:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    @staticmethod
    def fromvectors(v1, v2):
        return Mat2x2(v1.x, v2.x, v1.y, v2.y)

    def determinant(self):
        return (self.a * self.d) - (self.b * self.c)

    #Scalar multiplication
    def __rmul__(self, other):
        return Mat2x2(
            other * self.a,
            other * self.b,
            other * self.c,
            other * self.d
        )

    #Vector multiplication
    def __mul__(self, other):
        return Vector3(
            (self.a * other.x) + (self.b * other.y),
            (self.c * other.x) + (self.d * other.y)
        )

    def __str__(self):
        return "<Matrix2x2: \n [ {}, {}\n   {}, {} ]\n>".format(
            self.a,
            self.b,
            self.c,
            self.d
        )

    def inverse(self):
        if self.determinant() == 0:
            return None

        return (1 / self.determinant()) * Mat2x2(
            self.d,
            -self.b,
            -self.c,
            self.a
        )