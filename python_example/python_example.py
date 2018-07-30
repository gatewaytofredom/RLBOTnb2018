import math
from fieldstate import FieldState
from vector3 import Vector3

import kickoff

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket



class PythonExample(BaseAgent):
    
    def initialize_agent(self):
        #This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

        #Variable container for state of bot:
        #   WAITING - waiting for match start
        #   KICKOFF - kickoff run
        #   RUNNING - Normal play state
        self.GAMESTATE = "WAITING"

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        
        fieldstate = FieldState(packet, self)

<<<<<<< HEAD
        ball_location = Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y)
        
        car_location = Vector3(my_car.physics.location.x, my_car.physics.location.y)
        car_direction = get_car_facing_vector(my_car)
        car_to_ball = ball_location - car_location

        steer_correction_radians = car_direction.correction_to(car_to_ball)

        #normalize distence to ball to determine car throttle
        distence_to_ball = car_to_ball.length()
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
=======
        if self.GAMESTATE == "WAITING":
            pass 
        if self.GAMESTATE == "KICKOFF":
            return kickoff.run(packet)
        if self.GAMESTATE == "RUNNING":
            pass

        #Output nothing if state is not defined
        self.controller_state.throttle = 0
        self.controller_state.steer = 0
>>>>>>> bc80c323bee4f0a973761286578d83ff0442cc43

        return self.controller_state


#PID for turning the bot
def update_turning_pid(car_location,ball_location):
    angle_dif = Vector3.angle_between(car_location,ball_location)








    
