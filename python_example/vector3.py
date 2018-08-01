import math

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, val):
        return Vector3(self.x + val.x, self.y + val.y, self.z + val.z)

    def __sub__(self, val):
        return Vector3(self.x - val.x, self.y - val.y, self.z - val.z)

    def __mul__(self, val):
        val = float(val)
        return Vector3(val * self.x, val * self.y, val * self.z)

    def __rmul__(self, val):
        return self.__mul__(val)

    def correction_to(self, ideal):
        # The in-game axes are left handed, so use -x
        current_in_radians = math.atan2(self.y, -self.x)
        ideal_in_radians = math.atan2(ideal.y, -ideal.x)

        correction = ideal_in_radians - current_in_radians

        # Make sure we go the 'short way'
        if abs(correction) > math.pi:
            if correction < 0:
                correction += 2 * math.pi
            else:
                correction -= 2 * math.pi

        return correction

    def length(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

    def normalize(self):
        return Vector3(self.x / self.length(), self.y / self.length(), self.z / self.length())

    def __str__(self):
        return "<Vector3 ({}, {}, {})>".format(
            self.x,
            self.y,
            self.z
        )

    #get difference in angles between 2 vector pairs
    @staticmethod
    def angle_between(vec1, vec2):
        return math.acos((Vector3.dot(vec1, vec2))/(vec1.length() * vec2.length()))
    
    @staticmethod
    def dot(vec1, vec2):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z)

    @staticmethod
    def cross(a, b):
        return Vector3(
            (a.y * b.z) - (a.z * b.y),
            (a.z * b.x) - (a.x * b.z),
            (a.x * b.y) - (a.y * b.x)
        )

    @staticmethod
    def i(): return Vector3(1, 0, 0)
    
    @staticmethod
    def j(): return Vector3(0, 1, 0)

    @staticmethod
    def k(): return Vector3(0, 0, 1)

    @staticmethod
    def zero(): return Vector3(0, 0 ,0)
