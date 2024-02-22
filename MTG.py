from icecream import ic
import random

DEBUG = True


def cyclic_shift(my_list, n):
  """
  Performs a cyclic shift of a list, starting at the nth index.

  Args:
      my_list: The list to be shifted.
      n: The index at which to start the shift.

  Returns:
      The cyclically shifted list.
  """
  list_len = len(my_list)
  n = n % list_len  # Handle cases where n is greater than the list length
  return my_list[n:] + my_list[:n]


class MagicTheGathering():

  def __init__(self):
    self.players = []
    self.active_players = []
    self.active_player = None
    self.turn_count = 0
    self.round_count = 0
    self.starting_player = None
    self.current_phase = None
    self.current_step = None
    self.combat_occured = None
    self.step_registry = {
        'Untap Step': UntapStep,
        'Upkeep Step': UpkeepStep,
        'Draw Step': DrawStep,
        'Pre-Combat Main Phase': MainPhase,
        'Beginning of Combat Step': BeginningOfCombatStep,
        'Declare Attackers Step': DeclareAttackersStep,
        'Declare Blockers Step': DeclareBlockersStep,
        'Calculate Damage Step': CalculateDamageStep,
        'Post-Combat Main Phase': MainPhase,
        'End of Combat Step': EndOfCombatStep,
        'End Step': EndStep,
        'Cleanup Step': CleanupStep
    }
    self.phase_dictionary = {}
    self.stack = []

  def add_player(self, player=None):
    if player is not None:
      if self.players is None:
        self.players = []
      if self.active_players is None:
        self.active_players = []
      self.players.append(player)
      self.active_players.append(player)
    return None

  def start_game(self):
    self.game_loop()

  def determine_starting_player(self):
    if self.active_players is None or len(self.active_players) == 0:
      raise
    random.shuffle(self.active_players)
    self.starting_player = self.active_players[0]
    self.active_players[0].is_starting_player = True
    return (self.starting_player)

  def start_turn(self, player=None):
    if player is None:
      raise
    player.is_active_player = True
    self.active_player = player
    self.combat_occured = False
    self.turn_count += 1
    pass

  def game_loop(self):
    game_over = False
    while not game_over:
      if self.current_step is None:
        self.current_phase = "Beginning Phase"
        self.current_step = "Untap Step"
      if self.starting_player is None:
        self.round_count += 1
        self.start_turn(self.determine_starting_player())
      step_class = self.step_registry[self.current_step]
      current_step = step_class(game=self)
      current_step.execute()
      if self.current_step == 'Cleanup Step':
        self.start_turn(self.next_turn())
      self.advance_step()

  def advance_step(self):
    if self.current_step is None:
      raise
    all_steps = list(self.step_registry.keys())
    current_step_index = all_steps.index(self.current_step)
    #current_phase_index =
    next_step_index = (current_step_index + 1) % len(all_steps)
    self.current_step = all_steps[next_step_index]
    #self.current_phase = all_phases[next_phase_index]
    pass

  def next_turn(self):
    curent_player_index = self.active_players.index(self.active_player)
    next_player_index = (((
        (curent_player_index + 1) + 1) % len(self.active_players)) - 1)
    if DEBUG:
      ic(next_player_index)
      turn_order = [player.name for player in self.active_players]
      ic(turn_order)
    if next_player_index == 0 and curent_player_index == len(
        self.active_players) - 1:
      self.round_count += 1
    return self.active_players[next_player_index]


class Step():

  def __init__(self, game: MagicTheGathering | None = None, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)
    self.game = game
    self.priority_passed = False
    pass

  def execute(self):
    #https://mtg.fandom.com/wiki/Turn-based_action
    self.turn_based_actions()
    pass

  def reset_table_priority(self):
    for player in self.game.active_players:
      player.priority_passed = False
    self.priority_passed = False
    pass

  def step_loop(self, active_player=None, reset=None):
    if active_player is None:
      active_player = self.game.active_player
    while self.priority_passed is False:
      apnap_turn_order = cyclic_shift(
          self.game.active_players,
          self.game.active_players.index(active_player))
      for player in apnap_turn_order:
        if player.priority_passed is False:
          self.check_priority(player)
        if all(player.priority_passed is True
               for player in apnap_turn_order) is True:
          self.priority_passed = True
    if reset is not True:
      self.reset_table_priority()
    pass

  def check_priority(self, player):
    self.check_state_based_actions()
    print(f"Checking priority for {player}")
    priority_check = input("Pause")
    if priority_check.lower() == 'y':
      player.priority_passed = True
    if player.priority_passed is False:
      self.reset_table_priority()
      self.step_loop(player, reset=True)
    pass

  def check_state_based_actions(self):
    #https://mtg.fandom.com/wiki/State-based_action
    print(f"Checking state based actions")
    pass


class UntapStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    if game is None:
      raise
    print(f"Turn Count: {self.game.turn_count}")
    print(f"Round Count: {self.game.round_count}")
    print(f"{self.game.active_player.name}: Untapping...")
    #self.step_loop()
    pass


class UpkeepStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Upkeeping...")
    self.step_loop()
    pass


class DrawStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Drawing Card...")
    self.step_loop()
    pass


class MainPhase(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    if self.game.combat_occured is True:
      self.execute_post_combat_main_phase()
    if self.game.combat_occured is None or self.game.combat_occured is False:
      self.execute_pre_combat_main_phase()
    pass

  def execute_post_combat_main_phase(self):
    print(f"{self.game.active_player.name}: Post-Combat Main Phase...")
    self.step_loop()
    pass

  def execute_pre_combat_main_phase(self):
    print(f"{self.game.active_player.name}: Pre-Combat Main Phase...")
    self.step_loop()
    pass


class BeginningOfCombatStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    self.game.combat_occured = True
    print(f"{self.game.active_player.name}: Beginning Combat...")
    self.step_loop()
    pass


class DeclareAttackersStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Declaring Attackers...")
    self.step_loop()
    pass


class DeclareBlockersStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Declaring Blockers...")
    self.step_loop()
    pass


class CalculateDamageStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Calculating Damage...")
    self.step_loop()
    pass


class EndOfCombatStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Ending Combat...")
    self.step_loop()
    pass


class EndStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Ending Turn...")
    self.step_loop()
    pass


class CleanupStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Cleaning Up Turn...")
    input("Pause")
    pass


class Player():

  def __init__(self, name):
    self.name = name
    self.is_active_player = False
    self.is_starting_player = False
    self.priority_passed = False
    pass

  def __str__(self):
    return self.name


if __name__ == "__main__":
  game = MagicTheGathering()
  game.add_player(Player(name='Alice'))
  game.add_player(Player(name="Bob"))
  game.add_player(Player(name="Joe"))
  game.add_player(Player(name="Tim"))
  game.start_game()
