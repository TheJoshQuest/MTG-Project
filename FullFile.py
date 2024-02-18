from __future__ import annotations
from icecream import ic
import random

DEBUG = True
PERMANENTTYPES = [
    'Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'
]
ZONETYPES = [
    'Library', 'Hand', 'Battlefield', 'Graveyard', 'Stack', 'Exile',
    'CommandZone', 'Ante', 'OutsideTheGame', 'Sideboard', 'ContraptionDeck',
    'Sprockets', 'Scrapyard',
    'AbsolutelyRemovedFromTheFreakingGameForeverZone', 'AttractionDeck',
    'Junkyard', 'WhammyZone', 'InterplanarBattlefield'
]

'global PERMANENTTYPES'
PERMANENTTYPES = [
    'Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'
]

def trace_function(func):
    def wrapper(*args, **kwargs):
        'print(f"Entering function: {func.__name__}")'
        result = func(*args, **kwargs)
        'print(f"Exiting function: {func.__name__}")'
        return result
    return wrapper


class Player():

  def __init__(self, name, decks: dict = {}) -> None:
    self.name = name
    self.decks = decks
    self.is_active_player = False
    self.priority = False
    self.is_starting_player = False
    self.passed_priority = False
    return None

  def add_deck(self, deck_name='', deck=None):
    if deck is not None:
      deck_name = deck.name
    self.decks[deck_name] = deck

  def select_deck(self, deck_name='', deck=None, owner=None):
    if deck is not None:
      deck_name = deck.name
    if owner is None:
      owner = self
    self.library = Library(deck=self.decks[deck_name], owner=owner)
    self.hand = Hand(owner=owner)
    self.graveyard = Graveyard(owner=owner)

  def draw(self, num_cards=1):
    i = 0
    while i < num_cards:
      self.library.draw_card(self)
      i += 1


class Deck():

  def __init__(self, name='', cards=[]) -> None:
    self.name = name
    self.cards = cards
    return None


class GameObject():
  #@trace_function
  def __init__(self,
               name='',
               color=[],
               text=None,
               cardtype=None,
               printedpower=None,
               printedtoughness=None,
               owner=None,
               controller=None):
    self.name = name
    self.color = color
    self.text = text
    self.cardtype = cardtype
    self.printedpower = printedpower
    self.printedtoughness = printedtoughness
    self.active_component = CardComponent(parent_card=self)
    self.owner = owner
    self.controller = controller
    self.components = {
        "spell": SpellComponent(parent_card=self),
        "permanent": PermanentComponent(parent_card=self),
        "ability": AbilityComponent(parent_card=self),
        "card": CardComponent(parent_card=self)
    }
    return None

  #@trace_function
  def __str__(self) -> str:
    return f'{self.name}'


class Card(GameObject):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return None

  #@trace_function
  def can_cast_spell(self):
    return True

  #@trace_function
  def cast_spell(self, hand, stack):
    if self.can_cast_spell():
      hand.remove_card(self)
      self.components["spell"].activate_component()
      stack.add_card(self)
    return self, hand, stack


class Component():

  #@trace_function
  def __init__(self, parent_card):
    self.parent_card = parent_card
    return None

  #@trace_function
  def activate_component(self):
    self.parent_card.active_component = self
    return self.parent_card.active_component


class CardComponent(Component):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return None


class SpellComponent(Component):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return None

  #@trace_function
  def resolve_spell(self, stack, battlefield):
    stack.remove_card(self.parent_card)
    if any(cardtype in self.parent_card.cardtype
           for cardtype in PERMANENTTYPES):
      self.parent_card.components["permanent"].activate_component()
      battlefield.add_card(self.parent_card)
      self.parent_card.active_component.on_enters_battlefield()
    else:
      self.parent_card.components["card"].activate_component()
      self.parent_card.owner.graveyard.add_card(self.parent_card)
    return self.parent_card.active_component


class PermanentComponent(Component):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.base_power = self.parent_card.printedpower
    self.base_toughness = self.parent_card.printedtoughness
    self.power = self.base_power
    self.toughness = self.base_toughness
    self.tapped = None
    self.is_attacking = None
    return None

  #@trace_function
  def on_enters_battlefield(self):
    self.power += 1
    self.toughness += 1

  def tap(self):
    self.tapped = True
    pass

  def untap(self):
    self.tapped = False
    pass

  def declare_attacker(self):
    self.is_attacking = True
    self.tap()
    pass


class AbilityComponent(Component):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return None

  #@trace_function
  def activate_ability(self):
    pass

  #@trace_function
  def resolve_ability(self):
    pass


'''
class Spell(Card):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def resolve_spell(self,stack,battlefield,graveyard):
        stack.remove_card(self)
        if self.cardtype in PERMANENTTYPES:
            battlefield.add_card(self)
            self.on_enters_battlefield()
        else:
            graveyard.add_card(self)
'''
'''
class Permanent(GameObject):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def on_enters_battlefield(self):
        self.power += 1
        self.toughness += 1

class Creature(Permanent):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.originalpower = self.printedpower
        self.originaltoughness = self.printedpower
        self.power = self.originalpower
        self.toughness = self.originaltoughness

    def on_enters_battlefield(self):
        self.power += 1
        self.toughness += 1
'''


class Zone():

  #@trace_function
  def __init__(self,
               publiczone: bool = True,
               sharedzone: bool = True,
               orderedzone: bool = False):
    self.name = ''
    self.cards = []
    self.publiczone = publiczone
    self.sharedzone = sharedzone
    self.orderedzone = orderedzone
    return None

  #@trace_function
  def __str__(self):
    card_names = [card.name for card in self.cards]
    return f"{self.name}: {', '.join(card_names)}"

  #@trace_function
  def add_card(self, card):
    self.cards.append(card)
    return self.cards

  #@trace_function
  def remove_card(self, card):
    self.cards.remove(card)
    return self.cards


class Library(Zone):

  #@trace_function
  def __init__(self, deck=None, owner=None, **kwargs):
    super().__init__(publiczone=False,
                     sharedzone=False,
                     orderedzone=True,
                     **kwargs)
    self.name = 'Library'
    self.owner = owner
    if deck is not None:
      self.add_deck(deck, owner)
    return None

  #@trace_function
  def add_deck(self, deck, owner):
    for card in deck.cards:
      card.owner = owner
      self.add_card(card)
    return self

  #@trace_function
  def draw_card(self, player):
    hand = player.hand
    if len(self.cards) > 0:
      card_to_hand = self.cards[0]
      self.remove_card(card_to_hand)
      hand.add_card(card_to_hand)
    return self, hand

  #@trace_function
  def shuffle_library(self):
    random.shuffle(self.cards)
    return self


class Hand(Zone):

  #@trace_function
  def __init__(self, owner=None, **kwargs):
    super().__init__(publiczone=False, sharedzone=False)
    self.name = 'Hand'
    self.owner = owner

  def add_card(self, card):
    card.controller = self.owner
    super().add_card(card)
    return None


class Battlefield(Zone):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Battlefield'
    return None


class Graveyard(Zone):

  #@trace_function
  def __init__(self, owner=None, **kwargs):
    super().__init__(sharedzone=False, orderedzone=True, **kwargs)
    self.name = 'Graveyard'
    self.owner = owner
    return None


class Stack(Zone):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(orderedzone=True, **kwargs)
    self.name = 'Stack'
    return None

  #@trace_function
  def resolve_stack(self, battlefield):
    activecomponent = self.cards[0].active_component
    type(activecomponent)
    if isinstance(activecomponent, SpellComponent):
      activecomponent.resolve_spell(self, battlefield)
    if isinstance(activecomponent, AbilityComponent):
      activecomponent.resolve_ability(self)
    return self, battlefield


class Exile(Zone):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Exile'
    return None


class CommandZone(Zone):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Command Zone'
    return None


class AnteZone(Zone):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Ante Zone'
    return None


class OutsideTheGame(Zone):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(publiczone=False, **kwargs)
    self.name = 'Outside the Game'
    return None


class Sideboard(OutsideTheGame):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(publiczone=False, **kwargs)
    self.name = 'Sideboard'
    return None


class ContraptionDeck(Library):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Contraption Deck'
    return None


class Sprockets(Battlefield):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Sprockets'
    return None


class Scrapyard(Graveyard):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Scrapyard'
    return None


class AbsolutelyRemovedFromTheFreakingGameForeverZone(Exile):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Absolutely Removed From The Freaking Game Forever Zone'
    return None


class AttractionDeck(Library):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Attraction Deck'
    return None


class Junkyard(Graveyard):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Junkyard'
    return None


class WhammyZone(Library):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(publiczone=False,
                     sharedzone=False,
                     orderedzone=True,
                     **kwargs)
    self.name = 'Whammy Zone'
    return None


class InterplanarBattlefield(Battlefield):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.name = 'Interplanar Battlefield'
    return None


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


test_creature = Card(name='Test Creature',
                     printedpower=1,
                     printedtoughness=1,
                     text='',
                     cardtype=['Creature'])
test_land = Card(name='Test Land', text='', cardtype=['Land'])
test_sorcery = Card(name='Test Sorcery', text='', cardtype=['Sorcery'])

Player1 = Player(name='Josh')
Deck1 = Deck(name='Test Deck', cards=[test_creature])
Game = MagicTheGathering()
Game.add_player(Player1)

Player1.add_deck(deck=Deck1)
Player1.select_deck(deck=Deck1)

Game.start_game()

