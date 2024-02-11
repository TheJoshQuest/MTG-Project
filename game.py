from zones import *
from testing import *
import random


class MagicTheGathering():
    @trace_function
    def __init__(self) -> None:
        self.battlefield = Battlefield()
        self.stack = Stack()
        self.exile = Exile()
        self.players = []
        self.format = ''
        self.turn_count = 0
        self.full_rotations = 0
        self.active_player = None
        self.current_step = None
        return None

    @trace_function
    def mulligan(self):
        pass

    @trace_function
    def determine_starting_player(self):
        starting_player = random.choice(self.players)
        starting_player.starting_player = True
        return starting_player

    @trace_function
    def start_game(self):
        self.start_turn(self.determine_starting_player())
        pass

    @trace_function
    def start_turn(self,player):
        self.turn_count += 1
        if player.starting_player == True:
            self.full_rotations += 1
        player.active_player = True
        self.active_player = player
        self.beginning_step()
        pass

    def next_step(self):
        phase_order = ['Beginning Phase','Pre-combat Main Phase','Combat Phase','Post-combat Main Phase','Ending Phase']
        index = self.current_step.index(self.current_step)


    def beginning_step(self):
        self.current_step = 'Beginning Step'
        while (self.stack.cards>0 and all(player.passed_priority for player in self.players)):
            self.stack.resolve_stack(self.battlefield)
        self.next_step()
        pass

    def cleanup_step(self):
        self.next_turn()
        pass

    def next_turn(self):
        self.active_player.active_player = False
        index = self.players.index(self.active_player)
        self.start_turn(self.players[(index + 1) % len(self.players)])
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