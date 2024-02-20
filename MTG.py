import random
from icecream import ic

DEBUG = True


class MagicTheGathering():

  def __init__(self):
    self.players = []
    self.active_player = None
    self.starting_player = None
    self.current_phase = None
    self.current_step = None
    self.step_registry = {
        'Untap Step': UntapStep,
        'Upkeep Step': UpkeepStep,
        'Draw Step': DrawStep,
        'Main Phase': MainPhase,
        'Beginning of Combat Step': BeginningOfCombatStep,
        'Declare Attackers Step': DeclareAttackersStep,
        'Declare Blockers Step': DeclareBlockersStep,
        'Calculate Damage Step': CalculateDamageStep,
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
      self.players.append(player)
    return None

  def start_game(self):
    self.current_phase = "Beginning Phase"
    self.current_step = "Untap Step"
    self.start_turn(self.determine_starting_player())
    self.game_loop()

  def determine_starting_player(self):
    if self.players is None:
      raise
    random.shuffle(self.players)
    self.starting_player = self.players[0]
    return (self.starting_player)

  def start_turn(self, player=None):
    if player is None:
      raise
    player.active_player = True
    self.active_player = player

  def game_loop(self):
    game_over = False
    while not game_over:
      if self.current_step is None:
        raise
      step_class = self.step_registry[self.current_step]
      current_step = step_class()
      current_step.execute(self)
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


class Step():

  def __init__(self):
    pass

  def execute(self, game):
    pass


class UntapStep(Step):

  def __init__(self):
    super().__init__()
    pass

  def execute(self, game):
    print(f"{game.active_player.name}: Untapping...")
    pass


class UpkeepStep(Step):

  def __init__(self):
    super().__init__()
    pass

  def execute(self, game):
    print(f"{game.active_player.name}: Upkeeping...")
    pass


class DrawStep(Step):

  def __init__(self):
    super().__init__()
    pass


class MainPhase(Step):

  def __init__(self):
    super().__init__()
    pass


class BeginningOfCombatStep(Step):

  def __init__(self):
    super().__init__()
    pass


class DeclareAttackersStep(Step):

  def __init__(self):
    super().__init__()
    pass


class DeclareBlockersStep(Step):

  def __init__(self):
    super().__init__()
    pass


class CalculateDamageStep(Step):

  def __init__(self):
    super().__init__()
    pass


class EndOfCombatStep(Step):

  def __init__(self):
    super().__init__()
    pass


class EndStep(Step):

  def __init__(self):
    super().__init__()
    pass


class CleanupStep(Step):

  def __init__(self):
    super().__init__()
    pass


class Player():

  def __init__(self, name):
    self.name = name
    pass


if __name__ == "__main__":
  game = MagicTheGathering()
  game.add_player(Player(name='Alice'))
  game.add_player(Player(name="Bob"))
  game.start_game()
