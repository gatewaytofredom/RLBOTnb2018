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
        derivative = (current - self.prev) / dt
        return (self.p * error) + (self.i * self.integral) + (self.d * derivative)


#The controller uses 2 kind of PIDs:
#Standard PIDs: Use velocity, heading setpoints
# These PIDs are doing most of the work
#Absolute (corrective) PIDs: Use absolute position, rotation
# Account for error accumulation

vel_pid = PID(0.04, 0.000000001, 0)
position_pid = PID(0.016, 0, 0)

heading_pid = PID(0.8, 0, 0)
heading_abs_pid = PID(0.1, 0.005, 0)

fi = open("test.csv", "w")
fi.write("{},{},{},{},{},{},{},{},{},{}\n".format(
    "Time",
    "Error Magnitude",
    "Goal x",
    "Goal y",
    "Car x",
    "Car y",
    "Goal velocity",
    "Car velocity",
    "Throttle",
    "Steer"
))

def run(packet, fieldstate, start_pose):
    if fieldstate.elapsed_time() < 8:
        print(str(fieldstate.elapsed_time()))
        return SimpleControllerState()

    goal_position = start_pose + f(fieldstate.elapsed_time() - 8)
    error_vector = goal_position - fieldstate.car_location()

    correction_angle = fieldstate.car_facing_vector().correction_to(
        error_vector
    )

    goal_velocity = der_f(fieldstate.elapsed_time() - 8)
    goal_angle = fieldstate.car_facing_vector().correction_to(
        der_f(fieldstate.elapsed_time() - 8)
    )

    output = SimpleControllerState()

    #velocity PID
    output.throttle = clamp(
        vel_pid.update(
            goal_velocity.length(),
            fieldstate.car_velocity().length(),
            fieldstate.delta_time()
        ) +
        position_pid.update(
            error_vector.length(),
            0,
            fieldstate.delta_time()
        ),
    1.0, -1.0)

    if output.throttle < 0:
        print("EEEEEEEEEEEEEEEE: {}".format(output.throttle))

    print("VELOCITY: {}".format(
        fieldstate.car_velocity().length()
    ))
    print("GOAL: {}".format(
        goal_velocity.length()
    ))

    #heading PID
    output.steer = clamp(
        heading_pid.update(
            -goal_angle * sign(output.throttle),
            0,
            fieldstate.delta_time()
        ) +
        heading_abs_pid.update(
            -correction_angle * sign(output.throttle),
            0,
            fieldstate.delta_time()
        ),
    1.0, -1.0)

    # print("THROTTLE: {}".format(output.throttle))
    # print("STEER: {}".format(output.steer))
    # print("FACING VECTOR: {}".format(fieldstate.car_facing_vector().normalize()))
    # print("ERROR VECTOR: {}".format(error_vector))
    # print("DOT PRODUCT: {}".format(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())))
    
    fi.write("{},{},{},{},{},{},{},{},{},{}\n".format(
        fieldstate.elapsed_time(),
        error_vector.length() * sign(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())),
        goal_position.x,
        goal_position.y,
        fieldstate.car_location().x,
        fieldstate.car_location().y,
        goal_velocity.length(),
        fieldstate.car_velocity().length(),
        output.throttle,
        output.steer
    ))

    # fi.write("{},{},{},{}\n".format(
    #     fieldstate.elapsed_time(), 
    #     error_vector.length() * 
    #     sign(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())), 
    #     output.throttle, output.steer)
    # )

    return output

def sign(val):
    if val == 0: return 1
    return int(abs(val) / val)

def clamp(val, maximum, minimum):
    r = min(val, maximum)
    r = max(r, minimum)
    return r

def f(t):
    # print("T: {}".format(t))
    return Vector3(
        -1500*math.sin(((2*math.pi)/10000) * 163 * 2 * math.pi * t),
        -163 * 2 * math.pi * t
    )

def der_f(t):
    return Vector3(
        -1500*((2*math.pi)/10000)*163*2*math.pi*math.cos(((2*math.pi)/10000) * 163 * 2 * math.pi * t), 
        -163 * 2 * math.pi
    )