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

        if self.GAMESTATE == "WAITING":
            pass 
        if self.GAMESTATE == "KICKOFF":
            return kickoff.run()
        if self.GAMESTATE == "RUNNING":
            pass

        #Output nothing if state is not defined
        self.controller_state.throttle = 0
        self.controller_state.steer = 0

        return self.controller_state








    
