import math
import time

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket


TEST_STATE = "LINEAR"
THROTTLE = 1

OUTFILE = "out{}{}.csv".format(TEST_STATE, THROTTLE)

class CharacterizationBot(BaseAgent):

    def initialize_agent(self):
        #This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.file = open(OUTFILE, "w")
        self.start_t = time.time()
        self.first = True

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        my_car = packet.game_cars[self.index]

        pos = Vector2(my_car.physics.location.x, my_car.physics.location.y)
        vel = Vector2(my_car.physics.velocity.x, my_car.physics.velocity.y)

        if self.first:
            self.first = False
            self.start_p = pos
            self.start_v = vel

        if TEST_STATE == "LINEAR":
            self.controller_state.throttle = THROTTLE
            out = "{},{},{}\n".format(
                time.time() - self.start_t,
                (pos - self.start_p).length(), 
                (vel - self.start_v).length()
            )
            self.file.write(out)
            print(out)

        elif TEST_STATE == "ANGULAR":
            pass

        return self.controller_state

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, val):
        return Vector2(self.x + val.x, self.y + val.y)

    def __sub__(self, val):
        return Vector2(self.x - val.x, self.y - val.y)

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
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


def get_car_facing_vector(car):
    pitch = float(car.physics.rotation.pitch)
    yaw = float(car.physics.rotation.yaw)

    facing_x = math.cos(pitch) * math.cos(yaw)
    facing_y = math.cos(pitch) * math.sin(yaw)

    return Vector2(facing_x, facing_y)

    
