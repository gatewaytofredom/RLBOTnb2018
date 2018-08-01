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

spline_start = 8
spline_scale = (1.0/5.0)
is_spline = False

state = "None"

# fi = open("test.csv", "w")
# fi.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
#     "Time",
#     "Error Magnitude",
#     "Goal x",
#     "Goal y",
#     "Car x",
#     "Car y",
#     "Goal velocity",
#     "Car velocity",
#     "Goal Angle",
#     "Current Angle",
#     "Velocity PID",
#     "Position PID",
#     "Tangent Angle PID",
#     "Absolute Angle PID",
#     "Throttle",
#     "Steer"
# ))

def run(packet, fieldstate):
    global is_spline, state
    #Early start control
    if fieldstate.elapsed_time() < 8:
        return SimpleControllerState()

    #The following logic was written at 2 am by a programmer that just wants to be done with this project
    #It's horrible, and I'm sorry.

    if (not is_spline) or h_spline.finished(fieldstate.elapsed_time() - spline_start, spline_scale):
        is_spline = False
        controller = SimpleControllerState()
        aim_vector = fieldstate.goal_pos() - fieldstate.ball_location()
        #persue ball if close
        car_to_ball = fieldstate.ball_location() - fieldstate.car_location()
        print(car_to_ball.length())

        if Vector3.dot(fieldstate.car_velocity(), car_to_ball.normalize()) >= (0.4 * fieldstate.car_velocity().length()) and (Vector3.dot(aim_vector, car_to_ball) >= -0.2):
            correction = -fieldstate.car_facing_vector().correction_to(car_to_ball)
            controller.steer = 5 * correction
            controller.throttle =  clamp(0.3 + Vector3.dot(fieldstate.car_facing_vector(), car_to_ball), 1.0, -1.0)
            if car_to_ball.length() < 500: controller.boost = True
            if car_to_ball.length() < 500: controller.jump = True
            #print("SUPER ATTACK")
            return controller


        if car_to_ball.length() < 2500 or (not fieldstate.car_in_field()):
            #if on wrong side, run away and try to reposition
            #if on right side, gfi
            if Vector3.dot(aim_vector, car_to_ball) <= 0:
                #run away to reposition
                target_pos = fieldstate.ball_location() - (5000 * sign(Vector3.dot(aim_vector, Vector3.j())) * Vector3.j())
                set_target(
                    fieldstate,
                    v_clamp(target_pos, Vector3(4096, 5140), Vector3(-4096, -5140)),
                    fieldstate.ball_location() - target_pos,
                    time_scale=(1.0/1.0)
                )
                #print("RETREAT")
                return SimpleControllerState()
            else:
                correction = -fieldstate.car_facing_vector().correction_to(car_to_ball)
                controller.steer = 5 * correction
                if (Vector3.dot(fieldstate.car_velocity().normalize(), car_to_ball.normalize()) <= 0.7) and (fieldstate.car_velocity().length() > 250):
                    controller.handbrake = True
                controller.throttle = clamp(0.2 + Vector3.dot(fieldstate.car_facing_vector(), car_to_ball), 1.0, -1.0)
                if car_to_ball.length() < 500: controller.boost = True
                if car_to_ball.length() < 450: controller.jump = True
                #print("ATTACK")
                return controller

        #set setpoint if far away
        set_target(
            fieldstate,
            v_clamp(fieldstate.ball_location() - (1000 * sign(Vector3.dot(aim_vector, Vector3.j())) * Vector3.j()), Vector3(4096, 5140), Vector3(-4096, -5140)),
            aim_vector,
            time_scale=(1.0/2.0)
        )
        #print("PATH")

    else:
        return hermite_update(fieldstate)

    return SimpleControllerState()


def hermite_update(fieldstate):
    spline_pos, spline_d = h_spline.get(fieldstate.elapsed_time() - spline_start, spline_scale)

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
    
    # fi.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
    #     fieldstate.elapsed_time(),
    #     error_vector.length() * sign(Vector3.dot(error_vector, fieldstate.car_facing_vector().normalize())),
    #     goal_position.x,
    #     goal_position.y,
    #     fieldstate.car_location().x,
    #     fieldstate.car_location().y,
    #     goal_velocity.length(),
    #     fieldstate.car_velocity().length(),
    #     math.atan2(spline_d.y, spline_d.x),
    #     math.atan2(fieldstate.car_facing_vector().y, fieldstate.car_facing_vector().x),
    #     vel_pid_out,
    #     position_pid_out,
    #     heading_pid_out,
    #     heading_abs_pid_out,
    #     output.throttle,
    #     output.steer
    # ))

    if goal_velocity.length() > 1400:
        output.boost = True

    return output


def set_target(fieldstate, point, rotation_v, time_scale=(1.0 / 5.0), spline_t=None, on_complete=None):
    global spline_start, h_spline, spline_scale, is_spline

    h_spline.p0 = fieldstate.car_location()
    h_spline.p1 = point
    h_spline.v0 = fieldstate.car_facing_vector()
    h_spline.v1 = rotation_v
    h_spline.on_complete = on_complete

    
    spline_scale = time_scale
    is_spline = True
    if spline_t is None:
        spline_start = fieldstate.elapsed_time()
    else:
        spline_start = spline_t


def sign(val):
    if val == 0: return 1
    return int(abs(val) / val)

def v_clamp(v, maxi, mini):
    vx = clamp(v.x, maxi.x, mini.x)
    vy = clamp(v.y, maxi.y, mini.y)
    vz = clamp(v.z, maxi.z, mini.z)
    return Vector3(vx, vy, vz)

def clamp(val, maximum, minimum):
    r = min(val, maximum)
    r = max(r, minimum)
    return r

def f(t):
    return Vector3(
        500 * t,
        500 * t
    )

def der_f(t):
    return Vector3(
        500,
        500
    )