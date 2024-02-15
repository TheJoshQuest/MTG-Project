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
        else:
            phase_order = ['Beginning Phase','Pre-combat Main Phase','Combat Phase','Post-combat Main Phase','Ending Phase']
            beginning_phase_order = ['Untap Step','Upkeep Step','Draw Step']
            main_phase_order = []
            combat_phase_order = ['Beginning of Combat Step, Declare Attackers Step, Declare Blockers Step, Calculate Damage Step, End of Combat Step']
            ending_phase_order = ['End Step', 'Cleanup Step']
            phase_dict = {'Beginning Phase':beginning_phase_order,
                        'Pre-combat Main Phase':main_phase_order,
                        'Combat Phase':combat_phase_order,
                        'Post-combat Main Phase':main_phase_order,
                        'Ending Phase':ending_phase_order}
            phase_index = phase_order.index(self.current_phase)
            step_order = phase_dict[self.current_phase]
            step_index = step_order.index(self.current_step)
            if step_index >= len(step_order)-1:
                next_step_index = 0
                next_phase_index = phase_index + 1
            else:
                next_step_index = step_index + 1
                next_phase_index = phase_index
            next_phase = phase_order[next_phase_index]
            step_order = phase_dict[next_phase]
            next_step = step_order[next_step_index]
            self.start_step(next_phase,next_step)

    def start_step(self,phase = None, step = None):
        step_dict = {'Beginning Phase': {'Untap Step': self.untap_step(),
                                         'Upkeep Step':self.upkeep_step(),
                                         'Draw Step':self.draw_step()
                                         },
                     'Pre-Combat Main Phase':self.main_phase()
                    }
        
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