import random
from testing import trace_function
from zones import *
from icecream import ic

DEBUG = True


class MagicTheGathering():

  #@trace_function
  def __init__(self) -> None:
    self.battlefield = Battlefield()
    self.stack = Stack()
    self.exile = Exile()
    self.players = []
    self.format = ''
    self.turn_count = 0
    self.full_rotations = 0
    self.active_player = None
    self.starting_player = None
    self.current_phase = None
    self.current_step = None
    self.combat_this_turn = None
    self.step_dict = {
        'Beginning Phase': {
            'Untap Step': lambda: self.untap_step(),
            'Upkeep Step': lambda: self.upkeep_step(),
            'Draw Step': lambda: self.draw_step()
        },
        'Pre-combat Main Phase': {
            'Main Phase': lambda: self.main_phase()
        },
        'Combat Phase': {
            'Beginning of Combat Step':
            lambda: self.beginning_of_combat_step(),
            'Declare Attackers Step': lambda: self.declare_attackers_step(),
            'Declare Blockers Step': lambda: self.declare_blockers_step(),
            'Calculate Damage Step': lambda: self.calculate_damage_step(),
            'End of Combat Step': lambda: self.end_of_combat_step()
        },
        'Post-combat Main Phase': {
            'Main Phase': lambda: self.main_phase()
        },
        'Ending Phase': {
            'End Step': lambda: self.end_step(),
            'Cleanup Step': lambda: self.cleanup_step()
        }
    }

    self.phase_order = [
        'Beginning Phase', 'Pre-combat Main Phase', 'Combat Phase',
        'Post-combat Main Phase', 'Ending Phase'
    ]
    self.beginning_phase_order = ['Untap Step', 'Upkeep Step', 'Draw Step']
    self.main_phase_order = ['Main Phase']
    self.combat_phase_order = [
        'Beginning of Combat Step', 'Declare Attackers Step',
        'Declare Blockers Step', 'Calculate Damage Step', 'End of Combat Step'
    ]
    self.ending_phase_order = ['End Step', 'Cleanup Step']
    self.phase_dict = {
        'Beginning Phase': self.beginning_phase_order,
        'Pre-combat Main Phase': self.main_phase_order,
        'Combat Phase': self.combat_phase_order,
        'Post-combat Main Phase': self.main_phase_order,
        'Ending Phase': self.ending_phase_order
    }
    return None

  #@trace_function
  def mulligan(self):
    pass

  #@trace_function
  def determine_starting_player(self):
    starting_player = random.choice(self.players)
    starting_player.starting_player = True
    self.starting_player = starting_player
    return starting_player

  #@trace_function
  def start_game(self):
    for player in self.players:
      player.library.shuffle_library()
    self.start_turn(self.determine_starting_player())
    pass

  #@trace_function
  def start_turn(self, player):
    self.turn_count += 1
    if player.is_starting_player is True:
      self.full_rotations += 1
    player.active_player = True
    self.active_player = player
    self.combat_this_turn = False
    self.current_phase = None
    self.current_step = None
    self.next_step()
    pass

  def next_step(self):
    if self.current_phase is None and self.current_step is None:
      self.start_step('Beginning Phase', 'Untap Step')
    else:
      if self.current_phase is None:
        raise
      #ic(self.current_phase)
      phase_index = self.phase_order.index(self.current_phase)
      #ic(phase_index)
      step_order = self.phase_dict[self.current_phase]
      #ic(step_order)
      if self.current_step is not None:
        step_index = step_order.index(self.current_step)
      else:
        step_index = 1
      if step_index >= len(step_order) - 1:
        next_step_index = 0
        next_phase_index = phase_index + 1
      else:
        next_step_index = step_index + 1
        next_phase_index = phase_index
      next_phase = self.phase_order[next_phase_index]
      self.step_order = self.phase_dict[next_phase]
      next_step = None
      if len(step_order) > 0:
        next_step = self.step_order[next_step_index]
      #ic(next_phase)
      #ic(next_step)
      if self.current_step == 'Cleanup Step':
        self.next_turn()
      else:
        self.start_step(phase=next_phase, step=next_step)
      return None

  def start_step(self, phase=None, step=None):
    #ic(phase)
    #ic(step)
    if phase is None:
      raise
    if ("Main Phase" not in phase) and step is None:
      raise
    #ic(step_dict)
    #ic(step_dict[phase])
    #ic(step_dict.get(phase, False))
    valid_phase = self.step_dict.get(phase, False)
    if step is None:
      step = 'Main Phase'

    if isinstance(valid_phase, dict):
      valid_step = valid_phase.get(step, None)
      if valid_step is not None:
        valid_step()
    elif callable(valid_phase):
      valid_phase()

    #ic("Done")
    return None

  def hold_priority(self):
    if self.active_player is None:
      raise
    for i, item in enumerate(self.active_player.hand.cards):
      print(f'{i+1}: {item}')
      if i == len(self.active_player.hand.cards) - 1:
        print(f'{i+2}: {"Next Step"}')
    if len(self.active_player.hand.cards) == 0:
      print(f'{1}: {"Next Step"}')
    index = int(input('Select a card to cast: ')) - 1
    if 0 <= index < len(self.active_player.hand.cards):
      selected_card = self.active_player.hand.cards[index]
      print(f'Casting {selected_card}')
      selected_card.cast_spell(self.active_player.hand, self.stack)
      return True
    if index >= len(self.active_player.hand.cards):
      if index == len(self.active_player.hand.cards):
        self.active_player.passed_priority = True
        print('Next Step')
        #self.active_player.library.draw_card(self.active_player)
        return False
      else:
        print('Invalid index')
    else:
      print('Invalid index')
    return False

  def turn_structure(self):
    if DEBUG:
      ic(self.current_step)
      ic(self.current_phase)
      ic(self.turn_count)
    priority_held = True
    passed_step = False
    while not (passed_step):
      while priority_held:
        priority_held = self.hold_priority()
        #ic(priority_held)
      while (len(self.stack.cards) > 0
             and all(player.passed_priority for player in self.players)):
        self.stack.resolve_stack(self.battlefield)
        #ic(len(self.stack.cards))
      #ic(len(self.stack.cards) == 0)
      #ic(all(player.passed_priority for player in self.players))
      if (len(self.stack.cards) == 0
          and all(player.passed_priority for player in self.players)):
        passed_step = True
      #ic(passed_step)
    return None

  def untap_step(self):
    self.current_phase = 'Beginning Phase'
    self.current_step = 'Untap Step'
    self.turn_structure()
    self.next_step()
    return None

  def upkeep_step(self):
    self.current_phase = 'Beginning Phase'
    self.current_step = 'Upkeep Step'
    self.turn_structure()
    self.next_step()
    pass

  def draw_step(self):
    self.current_phase = 'Beginning Phase'
    self.current_step = 'Draw Step'
    if self.active_player is None:
      raise
    self.active_player.draw()
    self.turn_structure()
    self.next_step()
    pass

  def main_phase(self):
    self.current_phase = 'Main Phase'
    self.current_step = 'Main Phase'
    #ic(self.combat_this_turn)
    if self.combat_this_turn is False:
      self.current_phase = 'Pre-combat Main Phase'
    else:
      self.current_phase = 'Post-combat Main Phase'
    self.turn_structure()
    self.next_step()
    pass

  def beginning_of_combat_step(self):
    self.current_phase = 'Combat Phase'
    self.current_step = 'Beginning of Combat Step'
    self.combat_this_turn = True
    self.turn_structure()
    self.next_step()
    pass

  def declare_attackers_step(self):
    self.current_phase = 'Combat Phase'
    self.current_step = 'Declare Attackers Step'
    self.turn_structure()
    self.next_step()
    pass

  def declare_blockers_step(self):
    self.current_phase = 'Combat Phase'
    self.current_step = 'Declare Blockers Step'
    self.turn_structure()
    self.next_step()
    pass

  def calculate_damage_step(self):
    self.current_phase = 'Combat Phase'
    self.current_step = 'Calculate Damage Step'
    self.turn_structure()
    self.next_step()
    pass

  def end_of_combat_step(self):
    self.current_phase = 'Combat Phase'
    self.current_step = 'End of Combat Step'
    self.turn_structure()
    self.next_step()
    pass

  def end_step(self):
    self.current_phase = 'Ending Phase'
    self.current_step = 'End Step'
    self.turn_structure()
    self.next_step()
    pass

  def cleanup_step(self):
    self.current_phase = 'Ending Phase'
    self.current_step = 'Cleanup Step'
    self.turn_structure()
    #self.next_step()
    self.next_turn()
    pass

  def next_turn(self):
    if self.active_player is None:
      raise
    self.active_player.is_active_player = False
    index = self.players.index(self.active_player)
    self.start_turn(self.players[(index + 1) % len(self.players)])
    pass

  def end_game(self):
    pass

  #@trace_function
  def add_player(self, player):
    self.players.append(player)
    pass


class Phase():

  #@trace_function
  def __init__(self) -> None:
    return None


class Step():

  #@trace_function
  def __init__(self) -> None:
    return None
