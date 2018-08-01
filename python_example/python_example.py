import math
from fieldstate import FieldState
from vector3 import Vector3
import time

import kickoff
import persuit

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
        self.GAMESTATE = "RUNNING"
        self.t = time.time()
        self.first_run = True

        self.fieldstate = FieldState()



    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        self.fieldstate.update(packet, self)

        if self.fieldstate.elapsed_time() < 5:
            return SimpleControllerState()

        if self.first_run:
            print("FIRST LOL {}".format(self.fieldstate.car_location()))
            self.first_run = False
            self.start_pose = self.fieldstate.car_location()
            persuit.h_spline.p0 = self.start_pose + (50 * self.fieldstate.car_facing_vector().normalize())
            persuit.h_spline.p1 = Vector3.zero()#self.fieldstate.ball_location()
            persuit.h_spline.v0 = self.fieldstate.car_facing_vector()
            persuit.h_spline.v1 = -1 * Vector3.j()

        if packet.game_ball.physics.location.x != 0 and packet.game_ball.physics.location.y !=0:
            self.GAMESTATE = "RUNNING"
        
        if self.GAMESTATE == "WAITING":
            pass 
        if self.GAMESTATE == "KICKOFF":
            return kickoff.run(packet, self.fieldstate)
        if self.GAMESTATE == "RUNNING":
            return persuit.run(packet, self.fieldstate, self.start_pose)

        #Output nothing if state is not defined
        self.controller_state.throttle = 0
        self.controller_state.steer = 0

        return self.controller_state







    
