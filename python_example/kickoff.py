import math
from vector3 import Vector3

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

def run(packet: GameTickPacket,fieldstate):

    throttle = 1
    boost = True

        # car_location = Vector3.car_location
        # car_direction = get_car_facing_vector(my_car)
        # car_to_ball = ball_location - car_location

    ball_location = Vector3(packet.game_ball.physics.location.x, packet.game_ball.physics.location.y)
    # print(str(ball_location.x) + " " + str(ball_location.y))
    car_to_ball = ball_location - fieldstate.car_location()

    car_direction = fieldstate.car_facing_vector()

    steer_correction_radians = car_direction.correction_to(car_to_ball)

    # angle_error = Vector3.correction_to(fieldstate.car_location(),fieldstate.ball_location())
    #print(steer_correction_radians)


    steer = -steer_correction_radians * 0.5

    # if steer_correction_radians > .08:
    #     steer = -.9
    # elif steer_correction_radians < -0.08:
    #     steer = .9
    # else:
    #     steer = 0


    a = SimpleControllerState()

    a.throttle = throttle
    a.boost = boost
    a.steer = steer
    return a

    