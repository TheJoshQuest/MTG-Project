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
        self.current_phase = None
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
        self.next_step()
        pass

    def next_step(self):
        if self.current_phase is None and self.current_step is None:
            self.start_step('Beginning Phase','Untap Step')
        phase_order = ['Beginning Phase','Pre-combat Main Phase','Combat Phase','Post-combat Main Phase','Ending Phase']
        beginning_phase_order = ['Untap Step','Upkeep Step','Draw Step']
        main_phase_order = []
        combat_phase_order = ['Beginning of Combat Step, Declare Attackers Step, Declare Blockers Step, Calculate Damage Step, End of Combat Step']
        ending_phase_order = ['End Step', 'Cleanup Step']
        phase_index = phase_order.index(self.current_phase)
        if self.current_phase == 'Beginning Phase':
            step_order = beginning_phase_order
        if self.current_phase == 'Combat Phase':
            step_order = combat_phase_order
        if self.current_phase == 'Ending Phase':
            step_order = ending_phase_order
        if step_order is None:
            step_order = main_phase_order
        

        next_phase = None
        next_step = None
        #step_index = phase_order
        #phase_index = 
        self.start_step(next_phase,next_step)

    def start_step(self,phase = None, step = None):
                
        
        pass

    def beginning_step(self):
        self.current_phase = 'Beginning Phase'
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