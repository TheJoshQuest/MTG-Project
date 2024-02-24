from icecream import ic
import random

DEBUG = False


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
    self.stack = Zone(name='Stack')
    self.exile = Zone(name='Exile')
    self.battlefield = Zone(name='Battlefield')

  def add_player(self, player=None):
    if player is not None:
      if self.players is None:
        self.players = []
      if self.active_players is None:
        self.active_players = []
      player.game = self
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
      if self.active_player not in self.active_players:
        self.current_step = 'Cleanup Step'
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
    if self.active_player in self.active_players:
      current_player_index = self.active_players.index(self.active_player)
    else:
      current_player_index = self.players.index(self.active_player)
      while self.players[current_player_index] not in self.active_players:
        current_player_index = self.players.index(self.active_player) - 1
    next_player_index = current_player_index + 1
    if next_player_index >= len(self.active_players):
      next_player_index = 0 + (len(self.active_players) - next_player_index)
    DEBUG = True
    if DEBUG:
      ic(next_player_index)
      turn_order = [player.name for player in self.active_players]
      ic(turn_order)
    if next_player_index == 0 and current_player_index == len(
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
    if issubclass(self.__class__, Step):
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
      if active_player not in self.game.active_players:
        for player in self.game.active_players:
          player.priority_passed = True
        break
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
    priority_hold_check = player.get_available_actions()
    if DEBUG:
      #print(f'{priority_hold_check}')
      pass
    if priority_hold_check is True:
      player.priority_passed = True
    if player.priority_passed is False:
      self.reset_table_priority()
      self.step_loop(player, reset=True)
    pass

  def check_state_based_actions(self):

    #https://mtg.fandom.com/wiki/State-based_action
    print(f"Checking state based actions")
    if DEBUG:
      #704.5a
      print(f"Checking if player has 0 or less life")
      #704.5b
      print(
          f"Checking if player tried to draw from a library with no cards in it"
      )
      #704.5c
      print(f"Checking if a player has 10 or more poison counters")
      #704.5d
      print(f"Checking if a token is in a zone other than the battlefield")
      #705.5e
      print(f"Checking if a copy of a spell is in a zone other than the stack")
      print(
          f"Checking if a copy of a card is in a zone other than the stack or the battlefield"
      )
      #704.5f
      print(f"Checking if any creature has toughness 0 or less")
      #704.5g
      print(f"Checking for lethal damage to creatures")
      #704.5h
      print(f"Checking for lethal deathtouch damage")
      #704.5i
      print(f"Checking if a planewalker has loyalty 0")
      #704.5j
      print(f"Checking for the Legend Rule")
      #704.5k
      print(f"Checking for the World Rule")
      #704.5m
      print(
          f"Checking if an aura is attached to an illegal object or player, or is not attached to an object or player"
      )
      #704.5n
      print(
          f"Checking if an Equipment or Fortification is attached to an illegal permanent or to a player."
      )
      #704.5p
      print(
          f"Checking if a battle or creature is attached to an object or player"
      )
      print(
          f"Checking if a non-battle, non-creature permanent that is not an Aura, Equipment, or Fortification is attached to an object or player"
      )
      #704.5q
      print(
          f"Checking if a permanent has both a +1/+1 counter and a -1/-1 counter on it."
      )
      #704.5r
      print(
          f"Checking if a permanent has an ability that says it can't have more than N counters of a certain kind on it"
      )
      #704.5s
      print(
          f"Checking if the number of lore counters on a Saga permanent is greater than or equal to its final chapter number, and it isn't the source of a chapter ability on the stack"
      )
      #704.5t
      print(
          f"Checking if a player's venture marker is on the bottommost room of a dungeon card, and it isn't the source of a room ability that is on the stack"
      )
      #704.5u
      print(
          f"Checking if a permanent with space sculptor and any creatures without a sector designation are on the battlefield"
      )
      #704.5v
      print(
          f"Checking if a battle has defense 0 and isn't the source of an ability that is on the stack"
      )
      #704.5w
      print(
          f"Checking if a battle has no player in the game designated as its protector and no attacking creatures are currently attacking it"
      )
      #704.5x
      print(
          f"Checking if a siege's controller is also its designated protector")
      #704.5y
      print(
          f"Checking if a permanent has more than one Role controlled by the same player attached to it"
      )
      #704.6a
      print(f"Checking if a team has 0 or less life")
      #704.6b
      print(f"Checking if a team has 15 or more poison counters")
      #704.6c
      print(
          f"Checking if a player has been dealt 21 or more combat damage by the same commander"
      )
      #704.6d
      print(
          f"Checking if a commander is in a graveyard or exile and that object was put into that zone since the last time state-based actions were checked"
      )
      #704.6e
      print(
          f"Checking a non-ongoing scheme card is face up in the command zone and no abilities of any scheme are on the stack"
      )
      #704.6f
      print(
          f"Checking if a phenomenon card is face up in the command zone and no abilities of any phenomenon are on the stack"
      )
      #2.5
      print(f"Checking if a player has the highest life total")
      print(f"\n\n")
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
    self.game.active_player.draw_card()
    if DEBUG:
      print(f"Drawn Card: {self.game.active_player.hand.card_list[-1].name}")
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

  def __init__(self, name=None, deck=None):
    self.name = name
    self.is_active_player = False
    self.is_starting_player = False
    self.priority_passed = False
    self.deck = deck
    self.hand = Zone(name='Hand')
    self.library = Zone(name='Library', deck=deck)
    self.graveyard = Zone(name='Graveyard')
    self.game = None
    self.lost_game = False
    pass

  def __str__(self):
    return self.name

  def get_available_actions(self):
    options = []
    for card in self.hand.card_list:
      options.append(card)
      pass
    options.append("Pass Priority")
    options.append("Concede")
    optionsdict = {}
    i = 0
    for option in options:
      optionsdict[i] = option
      i += 1
    for i in optionsdict:
      print(f"{i+1}: {optionsdict[i]}")
    passing = input("")
    try:
      passing = int(passing) - 1
    except:
      return True
    if optionsdict[passing] == 'Pass Priority':
      return True
    if optionsdict[passing] == 'Concede':
      self.lose_game()
      return True
    return False

  def lose_game(self):
    self.lost_game = True
    self.game.active_players.remove(self)
    #self.game.start_turn(self.game.next_turn())

  def draw_card(self, amount=1):
    while amount > 0:
      self.hand.add_card(self.library.remove_card())
      amount -= 1
    pass


class GameObject():

  def __init__(self,
               name=None,
               type=None,
               power=None,
               toughness=None,
               **kwargs):
    self.name = name
    self.type = type
    self.basepower = power
    self.basetoughness = toughness
    self.active_component = None
    self.components = {
        'Card': CardComponent(self),
        'Spell': SpellComponent(self),
        'Permanent': PermanentComponent(self),
    }
    for key, value in kwargs.items():
      setattr(self, key, value)
    pass

  def __str__(self) -> str:
    if self.name is not None:
      return f"{self.name}"
    return "None"

  pass


class Card(GameObject):

  def __init__(self, name=None, **kwargs):
    super().__init__(name=name)
    for key, value in kwargs.items():
      setattr(self, key, value)
    pass


class Component():

  def __init__(self, gameobject=None):
    self.parent_gameobject = gameobject
    pass

  pass


class CardComponent(Component):

  def __init__(self, gameobject=None):
    super().__init__(gameobject=gameobject)

  pass


class SpellComponent(Component):

  def __init__(self, gameobject=None):
    super().__init__(gameobject=gameobject)

  pass


class PermanentComponent(Component):

  def __init__(self, gameobject=None):
    super().__init__(gameobject=gameobject)

  pass


class Zone():

  def __init__(self, name=None, deck: list | None = None):
    self.name = name
    self.card_list = []
    if self.name == 'Library':
      self.card_list = deck
    if self.name == 'Hand':
      self.card_list = []
    pass

  def __str__(self) -> str:
    if self.name is not None:
      return f"{self.name}"
    return "None"

  def add_card(self, card=None):
    if card is None:
      raise
    if self.card_list is None:
      raise
    self.card_list.append(card)
    pass

  def remove_card(self, card=None):
    if card is None:
      card = self.card_list[0]
    if self.card_list is None:
      raise
    self.card_list.remove(card)
    return card


if __name__ == "__main__":
  test_creature = Card(name='Test Creature',
                       type='Creature',
                       power=1,
                       toughness=1)
  deck_1 = [test_creature]
  deck_2 = [test_creature]
  deck_3 = [test_creature]
  deck_4 = [test_creature]
  player_1 = Player(name='Alice', deck=deck_1)
  player_2 = Player(name='Bob', deck=deck_2)
  player_3 = Player(name='Joe', deck=deck_3)
  player_4 = Player(name='Tim', deck=deck_4)
  game = MagicTheGathering()
  game.add_player(player_1)
  game.add_player(player_2)
  game.add_player(player_3)
  game.add_player(player_4)
  game.start_game()
