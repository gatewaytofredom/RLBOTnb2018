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

    #get difference in angles between 2 vector pairs
    @staticmethod
    def angle_between(vec1, vec2):
        return math.acos((Vector3.dot(vec1, vec2))/(vec1.length() * vec2.length()))
    
    @staticmethod
    def dot(vec1, vec2):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z)
