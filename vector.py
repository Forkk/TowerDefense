# vim: set expandtab ts=4 sw=4 softtabstop=4:

class Vector(tuple):
    def __new__(cls, x, y=None):
        # Hacky hacky hackity hack!
        if y != None:
            return super(Vector, cls).__new__(cls, (x, y))
        else:
            return super(Vector, cls).__new__(cls, (x[0], x[1]))


    def __add__(self, other):
        """
        Adds the components of the given vector or number to this vector's components.
        """
        if issubclass(other.__class__, tuple):
            return Vector(self[0] + other[0], self[1] + other[1])
        elif isinstance(other, (int, long, float, complex)):
            return Vector(self[0] + other, self[1] + other)
        else:
            raise TypeError("Can only add vectors or numbers to a vector.")

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

    def toIntVector(self):
        """
        Returns a copy of this vector with its components converted to integers.
        """
        return Vector(int(self[0]), int(self[1]))

