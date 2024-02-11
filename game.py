from zones import *
from testing import *


class MagicTheGathering():
    @trace_function
    def __init__(self) -> None:
        self.battlefield = Battlefield()
        self.stack = Stack()
        self.exile = Exile()
        self.players = []
        self.format = ''
        return None

    @trace_function
    def start_game(self):
        pass

    @trace_function
    def add_player(self,player):
        self.players.append(player)
        pass

class Phase():
    @trace_function
    def __init__(self) -> None:
        return None

class Step():
    @trace_function
    def __init__(self) -> None:
        return None