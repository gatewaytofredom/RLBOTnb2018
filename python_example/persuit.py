import math
import time

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from vector3 import Vector3

class PID:
    def __init__(self, p, i, d):
        self.p  = p
        self.i = i
        self.d = d

        self.integral = 0
        self.prev = 0
    
    def update(self, goal, current, dt):
        error = goal - current
        self.integral += error * dt
        derivative = (current - self.prev) * dt
        return (self.p * error) + (self.i * self.integral) + (self.d * derivative)


vel_pid = PID(0.1, 0, 0)
heading_pid = PID(0.5, 0, 0)

fi = open("test.csv", "w")

def run(packet, fieldstate, start_pose):
    if fieldstate.elapsed_time() < 8:
        return SimpleControllerState()

    goal_position = start_pose + f(time.time() - fieldstate.start_time - 8)
    error_vector = goal_position - fieldstate.car_location()
    output = SimpleControllerState()

    #velocity PID
    output.throttle = clamp(
        vel_pid.update(
            error_vector.length() * 
            sign(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())),
            0,
            fieldstate.delta_time()
        ),
    1.0, -1.0)

    correction_angle = fieldstate.car_facing_vector().correction_to(error_vector)

    #heading PID
    output.steer = clamp(
            heading_pid.update(
            correction_angle * sign(output.throttle),
            0,
            fieldstate.delta_time()
        ),
    1.0, -1.0)

    print("THROTTLE: {}".format(output.throttle))
    print("STEER: {}".format(output.steer))
    
    fi.write("{},{},{},{}\n".format(
        fieldstate.elapsed_time(), 
        error_vector.length() * 
        sign(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())), 
        output.throttle, output.steer)
    )

    return output

def sign(val):
    return int(abs(val) / val)

def clamp(val, maximum, minimum):
    r = min(val, maximum)
    r = max(r, minimum)
    return r

def f(t):
    return Vector3(
        -50 * t, 
        -50 * t
    )