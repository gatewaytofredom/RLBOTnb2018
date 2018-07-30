import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


class PythonExample(BaseAgent):

    old_value = 10000
    old_min = -16000
    old_max = 16000
    new_min = 0
    new_max = 100
    


    def initialize_agent(self):
        #This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        
        my_car = packet.game_cars[self.index]
        my_team = self.team

        ball_location = Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y)
        
        car_location = Vector3(my_car.physics.location.x, my_car.physics.location.y)
        car_direction = get_car_facing_vector(my_car)
        car_to_ball = ball_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_ball)

        #normalize distence to ball to determine car throttle
        distence_to_ball = math.sqrt(math.pow(car_to_ball.x,2) + math.pow(car_to_ball.y,2))
        print(distence_to_ball)
        if distence_to_ball < 8000:
            normalized = distence_to_ball/8000
            print("norm : "+str(distence_to_ball/8000))
        else:
            normalized = 1

        



        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -0.5  # Negative value for a turn to the left.
        else:
            turn = 0.5

        #Speed based on distence to ball
        self.controller_state.throttle = normalized
        self.controller_state.steer = turn

        return self.controller_state

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

    #get difference in angles between 2 vector pairs
    @staticmethod
    def angle_between(vec1, vec2):
        return math.acos((Vector3.dot(vec1, vec2))/(vec1.length() * vec2.length()))
    
    @staticmethod
    def dot(vec1, vec2):
        return (vec1.x * vec2.x) + (vec1.y * vec2.y) + (vec1.z * vec2.z)

def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector3(facing_x, facing_y)

#This is where you want the car to deliver the ball too
#could be to a goal or a team-mate
def ball_ideal_cords(x,y):
    ball_ideal_cords = Vector3(x,y)
    return ball_ideal_cords








    
