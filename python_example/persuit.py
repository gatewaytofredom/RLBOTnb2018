import math
import time

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from vector3 import Vector3
from splines import HermiteSpline

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
        derivative = 0
        if self.d != 0:
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

h_spline = HermiteSpline(None, None, None, None)

fi = open("test.csv", "w")
fi.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
    "Time",
    "Error Magnitude",
    "Goal x",
    "Goal y",
    "Car x",
    "Car y",
    "Goal velocity",
    "Car velocity",
    "Goal Angle",
    "Current Angle",
    "Velocity PID",
    "Position PID",
    "Tangent Angle PID",
    "Absolute Angle PID",
    "Throttle",
    "Steer"
))

def run(packet, fieldstate, start_pose):
    if fieldstate.elapsed_time() < 8:
        print(str(fieldstate.elapsed_time()))
        return SimpleControllerState()


    spline_pos, spline_d = h_spline.get(fieldstate.elapsed_time() - 8, (1.0 / 5.0))
    # spline_pos, spline_d = (f(fieldstate.elapsed_time() - 8, (1.0)), der_f(fieldstate.elapsed_time() - 8, (1.0)))

    print("TRANSFORMED SPLINE: {}".format(
        spline_pos
    ))
    print("CURRENT CAR POS: {}".format(
        fieldstate.car_location()
    ))

    goal_position = spline_pos
    error_vector = goal_position - fieldstate.car_location()

    correction_angle = fieldstate.car_facing_vector().correction_to(
        error_vector
    )

    goal_velocity = spline_d
    goal_angle = fieldstate.car_facing_vector().correction_to(
        spline_d
    )

    output = SimpleControllerState()

    #velocity PID
    vel_pid_out = vel_pid.update(
        goal_velocity.length(),
        fieldstate.car_velocity().length(),
        fieldstate.delta_time()
    )

    position_pid_out = position_pid.update(
        error_vector.length(),
        0,
        fieldstate.delta_time()
    )


    output.throttle = clamp(vel_pid_out + position_pid_out, 1.0, -1.0)

    if output.throttle < 0:
        print("EEEEEEEEEEEEEEEE: {}".format(output.throttle))



    #heading PID

    heading_pid_out = heading_pid.update(
        -goal_angle * sign(output.throttle),
        0,
        fieldstate.delta_time()
    )

    heading_abs_pid_out = heading_abs_pid.update(
        -correction_angle * sign(output.throttle),
        0,
        fieldstate.delta_time()
    )

    output.steer = clamp(heading_pid_out + heading_abs_pid_out, 1.0, -1.0)
    
    fi.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
        fieldstate.elapsed_time(),
        error_vector.length() * sign(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())),
        goal_position.x,
        goal_position.y,
        fieldstate.car_location().x,
        fieldstate.car_location().y,
        goal_velocity.length(),
        fieldstate.car_velocity().length(),
        math.atan2(spline_d.y, spline_d.x),
        math.atan2(fieldstate.car_facing_vector().y, fieldstate.car_facing_vector().x),
        vel_pid_out,
        position_pid_out,
        heading_pid_out,
        heading_abs_pid_out,
        output.throttle,
        output.steer
    ))

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
        500 * t,
        500 * t
    )

def der_f(t):
    return Vector3(
        500,
        500
    )