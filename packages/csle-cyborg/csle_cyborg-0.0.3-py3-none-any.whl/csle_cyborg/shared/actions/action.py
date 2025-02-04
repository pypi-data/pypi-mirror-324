# Copyright DST Group. Licensed under the MIT license.
from csle_cyborg.shared.observation import Observation
from csle_cyborg.simulator.state import State


class Action:

    def sim_execute(self, state: State) -> Observation:
        raise NotImplementedError

    def emu_execute(self) -> Observation:
        raise NotImplementedError

    def __str__(self):
        params = self.get_params()
        if "hostname" not in params:
            return f"{self.__class__.__name__.split('.')[-1]}"
        else:
            return f"{self.__class__.__name__.split('.')[-1]} {params['hostname']}"

    def get_params(self) -> dict:
        return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}

    @property
    def cost(self):
        return 0


class Sleep(Action):
    def sim_execute(self, state):
        return Observation()

    def emu_execute(self) -> Observation:
        return Observation()


class InvalidAction(Action):
    def __init__(self, action: Action):
        self.action = action

    def sim_execute(self, state):
        return Observation(success=False)

    def emu_execute(self) -> Observation:
        return Observation(success=False)

    @property
    def cost(self):
        return -0.1
