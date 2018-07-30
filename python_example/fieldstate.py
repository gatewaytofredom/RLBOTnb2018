import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from vector3 import Vector3

'''
Class for packaging game state into usable bits
'''
class FieldState:
    def __init__(self, packet: GameTickPacket, bot):
        self.packet = packet
        self.bot_car_index = bot.index
        self.bot_car = packet.game_cars[bot.index]
        self.team = bot.team

    def goal_pos(self):
        if self.team == 0:
            return (0,5120)
        else:
            return (0, -5120)

    def ball_location(self):
        return Vector3(
            self.packet.game_ball.physics.location.x,
            self.packet.game_ball.physics.location.y,
            self.packet.game_ball.physics.location.z
        )

    def car_location(self):
        return Vector3(
            self.bot_car.physics.location.x,
            self.bot_car.physics.location.y,
            self.bot_car.physics.location.z,
        )

    def car_facing_vector(self, car_index=None):
        car = None
        if car_index is None:
            car = self.bot_car
        else:
            car = self.packet.game_cars[car_index]

        pitch = float(car.physics.rotation.pitch)
        yaw = float(car.physics.rotation.yaw)

        facing_x = math.cos(pitch) * math.cos(yaw)
        facing_y = math.cos(pitch) * math.sin(yaw)

        return Vector3(facing_x, facing_y)