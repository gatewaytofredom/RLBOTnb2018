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

        if self.first_run:
            first_run = False
            self.start_pose = self.fieldstate.car_location()

        if self.GAMESTATE == "WAITING":
            pass 
        if self.GAMESTATE == "KICKOFF":
            return kickoff.run(packet)
        if self.GAMESTATE == "RUNNING":
            return persuit.run(packet, self.fieldstate, self.start_pose)

        #Output nothing if state is not defined
        self.controller_state.throttle = 0
        self.controller_state.steer = 0

        return self.controller_state








    
