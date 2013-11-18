# vim: set expandtab ts=4 sw=4 softtabstop=4:

import math

def toVector(t):
    """
    Converts the given coordinate tuple to a vector.
    """
    return Vector(t[0], t[1])

class Vector(tuple):
    def __new__(cls, x, y):
        return super(Vector, cls).__new__(cls, (x, y))


    def __add__(self, other):
        """
        Adds the components of the given vector or number to this vector's components.
        Note: You can only add a vector to a vector. For performance reasons, adding a number 
        to both of a vector's fields should be done via the add2() function.
        """
        return Vector(self[0] + other[0], self[1] + other[1])

    def __radd__(self, other):
        return __add__(self, other)

    def add2(self, num):
        return Vector(self[0] + num, self[1] + num)


    def __sub__(self, other):
        """
        Subtracts the components of the given vector or number from this vector's components.
        """
        if issubclass(other.__class__, tuple):
            return Vector(self[0] - other[0], self[1] - other[1])
        elif isinstance(other, (int, long, float, complex)):
            return Vector(self[0] - other, self[1] - other)
        else:
            raise TypeError("Can only subtract vectors or numbers from a vector.")

    def __rsub__(self, other):
        return __sub__(self, other)


    def __mul__(self, other):
        """
        Multiplies the components of this vector by the given vector or number.
        """
        if issubclass(other.__class__, tuple):
            return Vector(self[0] * other[0], self[1] * other[1])
        elif isinstance(other, (int, long, float, complex)):
            return Vector(self[0] * other, self[1] * other)
        else:
            raise TypeError("Can only multiply vectors by numbers or other vectors.")

    def __rmul__(self, other):
        return __mul__(self, other)


    def __div__(self, other):
        """
        Divides the components of this vector by the given vector or number.
        """
        if issubclass(other.__class__, tuple):
            return Vector(self[0] / other[0], self[1] / other[1])
        elif isinstance(other, (int, long, float, complex)):
            return Vector(self[0] / other, self[1] / other)
        else:
            raise TypeError("Can only divide vectors by numbers or other vectors.")

    def __rdiv__(self, other):
        return __div__(self, other)


    def __pow__(self, other):
        """
        Raises the components of this vector to the power of the components of the given vector or number.
        """
        if issubclass(other.__class__, tuple):
            return Vector(self[0] ** other[0], self[1] ** other[1])
        elif isinstance(other, (int, long, float, complex)):
            return Vector(self[0] ** other, self[1] ** other)
        else:
            raise TypeError("Can only power vectors by numbers or other vectors.")

    def __rpow__(self, other):
        return __pow__(self, other)


    def getLength(self):
        """
        Returns the length (or magnitude) of the vector.
        sqrt(x^2 + y^2)
        """
        return math.sqrt(self[0]**2 + self[1]**2)
    
    def getUnitVector(self):
        return self / self.getLength()

    def toIntVector(self):
        """
        Returns a copy of this vector with its components converted to integers.
        """
        return Vector(int(self[0]), int(self[1]))

