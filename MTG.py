import random
from icecream import ic

DEBUG = True


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

  def execute(self, game):
    pass

  def step_loop(self):
    pass


class UntapStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    if game is None:
      raise
    print(f"Turn Count: {self.game.turn_count}")
    print(f"Round Count: {self.game.round_count}")
    print(f"{self.game.active_player.name}: Untapping...")
    pass


class UpkeepStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Upkeeping...")
    pass


class DrawStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Drawing Card...")
    pass


class MainPhase(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    if self.game.combat_occured is True:
      self.execute_post_combat_main_phase()
    if self.game.combat_occured is None or self.game.combat_occured is False:
      self.execute_pre_combat_main_phase()
    pass

  def execute_post_combat_main_phase(self):
    print(f"{self.game.active_player.name}: Post-Combat Main Phase...")

  def execute_pre_combat_main_phase(self):
    print(f"{self.game.active_player.name}: Pre-Combat Main Phase...")


class BeginningOfCombatStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    self.game.combat_occured = True
    print(f"{self.game.active_player.name}: Beginning Combat...")
    pass


class DeclareAttackersStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Declaring Attackers...")
    pass


class DeclareBlockersStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Declaring Blockers...")
    pass


class CalculateDamageStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Calculating Damage...")
    pass


class EndOfCombatStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Ending Combat...")
    pass


class EndStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Ending Turn...")
    pass


class CleanupStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def execute(self):
    print(f"{self.game.active_player.name}: Cleaning Up Turn...")
    input("Pause")
    pass


class Player():

  def __init__(self, name):
    self.name = name
    self.is_active_player = None
    pass


if __name__ == "__main__":
  game = MagicTheGathering()
  game.add_player(Player(name='Alice'))
  game.add_player(Player(name="Bob"))
  game.add_player(Player(name="Joe"))
  game.add_player(Player(name="Tim"))
  game.start_game()
