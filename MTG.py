import copy
from icecream import ic
import random

DEBUG = False
PERMANENT_TYPES = [
    'Land', 'Enchantment', 'Creature', 'Battle', 'Artifact', 'Planeswalker'
]


def cyclic_shift(list, n):
  """
  Performs a cyclic shift of a list, starting at the nth index.

  Args:
      my_list: The list to be shifted.
      n: The index at which to start the shift.

  Returns:
      The cyclically shifted list.
  """
  list_len = len(list)
  n = n % list_len  # Handle cases where n is greater than the list length
  return list[n:] + list[:n]


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
    self.combat_occurred = None
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
    self.phase_dictionary = {
        'Untap Step': 'Beginning Phase',
        'Upkeep Step': 'Beginning Phase',
        'Draw Step': 'Beginning Phase',
        'Pre-Combat Main Phase': 'Main Phase',
        'Beginning of Combat Step': 'Combat Phase',
        'Declare Attackers Step': 'Combat Phase',
        'Declare Blockers Step': 'Combat Phase',
        'Calculate Damage Step': 'Combat Phase',
        'End of Combat Step': 'Combat Phase',
        'Post-Combat Main Phase': 'Main Phase',
        'End Step': 'End Phase',
        'Cleanup Step': 'End Phase'
    }
    self.stack = Zone(name='Stack', owner=self)
    self.exile = Zone(name='Exile', owner=self)
    self.battlefield = Zone(name='Battlefield', owner=self)

  def add_player(self, playerlist=None):
    if playerlist is not None:
      if self.players is None:
        self.players = []
      if self.active_players is None:
        self.active_players = []
    if isinstance(playerlist, Player):
      playerlist.game = self
      self.players.append(playerlist)
      self.active_players.append(playerlist)
    if isinstance(playerlist, list):
      for player in playerlist:
        self.add_player(player)
    return None

  def start_game(self):
    for player in self.active_players:
      for card in player.library.card_list:
        if DEBUG:
          print(f'{player}: {card.name}')
        card.owner = player
      player.draw_card(amount=7)
    self.perform_mulligans()
    self.game_loop()

  def perform_mulligans(self):
    pass

  def determine_starting_player(self):
    if self.active_players is None or len(self.active_players) == 0:
      raise
    random.shuffle(self.active_players)
    self.players = self.active_players.copy()
    self.starting_player = self.active_players[0]
    self.active_players[0].is_starting_player = True
    return (self.starting_player)

  def start_turn(self, player=None):
    if player is None:
      raise
    player.is_active_player = True
    self.active_player = player
    self.combat_occurred = False
    self.turn_count += 1
    pass

  def game_loop(self):
    self.game_over = False
    while not self.game_over:
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
    if len(self.active_players) == 1:
      self.winners = self.active_players[0]
      print(f"Game Over! {self.winners.name} wins!")

  def advance_step(self):
    if self.current_step is None:
      raise
    all_steps = list(self.step_registry.keys())
    all_phases_steps = list(self.phase_dictionary.keys())
    all_phases = list(self.phase_dictionary.values())
    current_step_index = all_steps.index(self.current_step)
    next_step_index = (current_step_index + 1) % len(all_steps)
    next_phase_index = all_phases_steps.index(all_steps[next_step_index])
    self.current_step = all_steps[next_step_index]
    self.current_phase = all_phases[next_phase_index]
    pass

  def next_turn(self, player=None):
    #DEBUG = True
    if DEBUG:
      ic(self.active_player.name)
      active_player_list = []
      player_list = []
      for playerdebug in self.players:
        player_list.append(playerdebug.name)
      for playerdebug in self.active_players:
        active_player_list.append(playerdebug.name)
      ic(player_list)
      ic(active_player_list)
    if player is not None:
      return player

    next_in_turn_order = self.players.index(self.active_player) + 1
    if next_in_turn_order >= len(self.active_players):
      try:
        self.players[next_in_turn_order]
      except IndexError:
        next_in_turn_order = 0
    if DEBUG:
      ic(next_in_turn_order)
      ic(self.players[next_in_turn_order].name)
      ic(self.active_players)
      ic(self.players[next_in_turn_order] not in self.active_players)

    while (self.players[next_in_turn_order] not in self.active_players):
      next_in_turn_order += 1
      if next_in_turn_order >= len(self.players):
        next_in_turn_order = 0
    if self.starting_player not in self.active_players:
      acting_starting_player = self.active_players[0]
    else:
      acting_starting_player = self.starting_player
    if (self.players[next_in_turn_order] == acting_starting_player) and (
        self.active_player != acting_starting_player):
      self.round_count += 1
    return self.players[next_in_turn_order]

  pass


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
    else:
      raise
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
        if active_player not in self.game.active_players:
          for participants in self.game.active_players:
            participants.priority_passed = True
        if player.priority_passed is False:
          if len(self.game.stack.card_list) > 0:
            stack_callout = ""
            for card in self.game.stack.card_list:
              stack_callout += card.name
              if card != self.game.stack.card_list[-1]:
                stack_callout += ", "
            print(f"Stack [{stack_callout}]")
          self.check_priority(player)
        if all(player.priority_passed is True
               for player in apnap_turn_order) is True:
          if len(self.game.stack.card_list) > 0:
            self.game.stack.resolve_stack()
            self.reset_table_priority()
          else:
            self.priority_passed = True
    if reset is not True:
      self.reset_table_priority()
    pass

  def check_priority(self, player):
    #DEBUG = True
    self.check_state_based_actions()
    print(f"Checking priority for {player}")
    priority_hold_check = player.get_available_actions()
    if DEBUG:
      print(f'{priority_hold_check}')
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
    #DEBUG2 = True
    if DEBUG:
      print(f"{len(self.game.active_players)}")
    if len(self.game.active_players) <= 1:
      if len(self.game.active_players) == 1:
        self.game.active_players[0].won_game = True
      self.game.game_over = True
    pass

  pass


class UntapStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    #DEBUG = True
    if game is None:
      raise
    print(f"Turn Count: {self.game.turn_count}")
    print(f"Round Count: {self.game.round_count}")
    print(f"{self.game.active_player.name}: Untapping...")
    if DEBUG:
      ic(len(self.game.battlefield.card_list))
      for card in self.game.battlefield.card_list:
        ic(card.name)
      ic(self.game.active_player.name)
    for permanent in self.game.battlefield.card_list:
      if DEBUG:
        ic(permanent.name)
        ic(permanent.controller.name)
      if permanent.controller == self.game.active_player:
        permanent.active_component.untap()
    #self.step_loop()
    pass

  pass


class UpkeepStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Upkeeping...")
    self.step_loop()
    pass

  pass


class DrawStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Drawing Card...")
    #DEBUG = True
    if DEBUG:
      ic(len(self.game.active_player.library.card_list))
    self.game.active_player.draw_card()
    if DEBUG:
      for card in self.game.active_player.hand.card_list:
        ic(print(f"Cards in hand {card.name}"))
      if len(self.game.active_player.hand.card_list) > 0:
        ic(
            print(
                f"Drawn Card: {self.game.active_player.hand.card_list[-1].name}"
            ))
    self.step_loop()
    pass

  pass


class MainPhase(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    if self.game.combat_occurred is True:
      self.execute_post_combat_main_phase()
    if self.game.combat_occurred is None or self.game.combat_occurred is False:
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

  pass


class BeginningOfCombatStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    self.game.combat_occurred = True
    print(f"{self.game.active_player.name}: Beginning Combat...")
    self.step_loop()
    pass

  pass


class DeclareAttackersStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Declaring Attackers...")
    self.step_loop()
    pass

  pass


class DeclareBlockersStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Declaring Blockers...")
    self.step_loop()
    pass

  pass


class CalculateDamageStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Calculating Damage...")
    self.step_loop()
    pass

  pass


class EndOfCombatStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Ending Combat...")
    self.step_loop()
    pass

  pass


class EndStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Ending Turn...")
    self.step_loop()
    pass

  pass


class CleanupStep(Step):

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    pass

  def turn_based_actions(self):
    print(f"{self.game.active_player.name}: Cleaning Up Turn...")
    input("Pause")
    pass

  pass


class Player():

  def __init__(self, name=None, deck=None):
    self.name = name
    self.is_active_player = False
    self.is_starting_player = False
    self.priority_passed = False
    self.deck = deck
    if deck is not None:
      for card in self.deck:
        card.owner = self
    self.hand = Zone(name='Hand', owner=self)
    self.library = Zone(name='Library', deck=deck, owner=self)
    self.graveyard = Zone(name='Graveyard', owner=self)
    self.game = None
    self.lost_game = False
    self.won_game = False
    pass

  def __str__(self):
    return self.name

  def get_available_actions(self):
    options = []
    for card in self.hand.card_list:
      if card.active_component.check_is_castable(self):
        options.append(card)
      pass
    options.append("Pass Priority")
    options.append("Concede")
    options_dict = {}
    i = 0
    for option in options:
      options_dict[i] = option
      i += 1
    for i in options_dict:
      print(f"{i+1}: {options_dict[i]}")
    passing = input("")
    try:
      passing = int(passing) - 1
    except:
      return True
    if passing < 0 or passing > len(options_dict):
      return False
    if options_dict[passing] == 'Pass Priority':
      return True
    if options_dict[passing] == 'Concede':
      self.lose_game()
      return True
    try:
      options_dict[passing].active_component.cast(self)
    except:
      return False
    try:
      options_dict[passing].active_component.activate(self)
    except:
      return False
    return False

  def lose_game(self):
    self.lost_game = True
    self.game.active_players.remove(self)
    if len(self.game.active_players) == 1:
      self.game.active_players[0].won_game = True
      self.game.game_over = True
    #self.game.start_turn(self.game.next_turn())

  pass

  def draw_card(self, amount=1):
    #DEBUG = True
    if DEBUG:
      ic(amount)
      ic(len(self.library.card_list))
      ic(len(self.hand.card_list))
    while amount > 0:
      self.hand.add_card(self.library.remove_card())
      amount -= 1
    if DEBUG:
      ic(amount)
      ic(len(self.library.card_list))
      ic(len(self.hand.card_list))
    pass

  def can_pay_cost(self, cost, type = 'Mana') -> bool:
    pass
  
  pass


class GameObject():

  def __init__(self,
               name=None,
               type=None,
               power=None,
               cost=None,
               toughness=None,
               owner=None,
               controller=None,
               **kwargs):
    self.name = name
    self.type = type
    self.base_power = power
    self.base_toughness = toughness
    self.active_component = None
    self.cost = cost
    self.owner = owner
    self.controller = controller
    if controller is None:
      self.controller = self.owner
    self.components = {
        'Card': CardComponent(self),
        'Spell': SpellComponent(self),
        'Permanent': PermanentComponent(self),
        'Ability': AbilityComponent(self)
    }
    self.current_zone = None
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
    self.components['Card'].activate_component()
    pass


class Component():

  def __init__(self, game_object: GameObject | None = None):
    self.parent_game_object = game_object
    pass

  def activate_component(self):
    self.parent_game_object.active_component = self
    pass

  def resolve(self):
    #DEBUG = True
    if not (isinstance(self, (SpellComponent, AbilityComponent))):
      return None
    self.parent_game_object.owner.game.stack.remove_card(
        self.parent_game_object)

    if self.parent_game_object.type in PERMANENT_TYPES:
      if isinstance(self.parent_game_object.owner, MagicTheGathering):
        self.parent_game_object.owner.battlefield.add_card(
            self.parent_game_object)
      else:
        self.parent_game_object.owner.game.battlefield.add_card(
            self.parent_game_object)
      self.parent_game_object.components['Permanent'].activate_component()
    else:
      self.parent_game_object.owner.graveyard.add_card(self.parent_game_object)

  def activate(self, player=None):
    pass

  pass


class CardComponent(Component):

  def __init__(self, game_object=None):
    super().__init__(game_object=game_object)
    self.activate_component()

  def cast(self, player=None):
    #DEBUG = True
    self.parent_game_object.current_zone.remove_card(self.parent_game_object)
    self.parent_game_object.components['Spell'].activate_component()
    if player is not None:
      self.parent_game_object.controller = player
    self.parent_game_object.owner.game.stack.add_card(self.parent_game_object)
    if DEBUG:
      ic(self.parent_game_object.owner.game.stack.card_list)
      ic(self.parent_game_object.controller)

  def check_is_castable(self, player=None):
    #DEBUG = True
    if player is None:
      return False
    is_main_phase = (
        self.parent_game_object.owner.game.current_phase == 'Main Phase')
    stack_is_empty = (len(
        self.parent_game_object.owner.game.stack.card_list) == 0)
    is_active_player = (
        player == self.parent_game_object.owner.game.active_player)
    is_not_no_cost = (self.parent_game.object.cost is not None)
    can_pay_cost = player.can_pay_cost(self.parent_game_object.cost, 'Mana')
      
    if DEBUG:
      ic(is_main_phase)
      ic(self.parent_game_object.owner.game.current_phase)
      ic(stack_is_empty)
      ic(len(self.parent_game_object.owner.game.stack.card_list))
      ic(is_active_player)
      ic(player.name)
      ic(self.parent_game_object.owner.game.active_player.name)
    is_castable = all([is_main_phase,
                       stack_is_empty,
                       is_active_player,
                       is_not_no_cost
                      ])
    return is_castable

  pass


class SpellComponent(Component):

  def __init__(self, game_object=None):
    super().__init__(game_object=game_object)

  pass


class PermanentComponent(Component):

  def __init__(self, game_object=None):
    super().__init__(game_object=game_object)
    self.is_tapped = False

  def untap(self):
    DEBUG = True
    if DEBUG:
      print(f'Untapping {self.parent_game_object.name}')
    self.is_tapped = False

  pass


class AbilityComponent(Component):

  def __init__(self, game_object=None):
    super().__init__(game_object=game_object)

  pass

class Effect():
  def __init__(self):
    pass

class Zone():

  def __init__(self,
               name=None,
               deck: list | None = None,
               owner: Player | MagicTheGathering | None = None):
    self.name = name
    self.owner = owner
    self.card_list = []
    if self.name == 'Library':
      self.card_list = deck
    pass

  def __str__(self) -> str:
    if self.name is not None:
      return f"{self.name}"
    return "None"

  def resolve_stack(self):
    if self.name != 'Stack':
      return None
    if len(self.card_list) == 0:
      return None
    self.card_list[0].active_component.resolve()

  def add_card(self, card=None):
    if card is None:
      return None
    if self.card_list is None:
      raise
    card.current_zone = self
    self.card_list.append(card)
    pass

  def remove_card(self, card=None):
    if self.card_list is None:
      raise
    if len(self.card_list) == 0 and self.name == 'Library':
      self.owner.drew_from_empty_library = True
      return None
    if card is None:
      card = self.card_list[0]
    card.current_zone = None
    self.card_list.remove(card)
    return card


class Deck():

  def __init__(self, name=''):
    self.name = name
    self.card_list = []
    pass

  #def __repr__(self):
  #return self.card_list

  def __str__(self):
    return self.name

  def add_card(self, cards=None):
    if isinstance(cards, Card):
      self.card_list.append(copy.deepcopy(cards))
    if isinstance(cards, list):
      for card in cards:
        self.add_card(card)

  def remove_card(self, card):
    if card in self.card_list:
      self.card_list.remove(card)

  pass

class Mana():
  def __init__(self,color = "Colorless", restriction = None):
    self.color = color
    self.restriction = restriction
  pass

if __name__ == "__main__":
  test_creature = Card(name='Test Creature',
                       type='Creature',
                       cost={'C': 0
                            }
                       power=1,
                       toughness=1)

  deck_1 = Deck(name='Deck 1')
  deck_1.add_card(test_creature)
  deck_2 = Deck(name='Deck 2')
  deck_2.add_card(test_creature)
  deck_3 = Deck(name='Deck 3')
  deck_3.add_card(test_creature)
  deck_4 = Deck(name='Deck 4')
  deck_4.add_card(test_creature)
  player_1 = Player(name='Alice', deck=deck_1.card_list)
  player_2 = Player(name='Bob', deck=deck_2.card_list)
  player_3 = Player(name='Joe', deck=deck_3.card_list)
  player_4 = Player(name='Tim', deck=deck_4.card_list)
  game = MagicTheGathering()
  game.add_player(player_1)
  game.add_player(player_2)
  game.add_player(player_3)
  game.add_player(player_4)
  game.start_game()
