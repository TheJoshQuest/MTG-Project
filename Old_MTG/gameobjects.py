from icecream import ic
from testing import *
import random
from datetime import datetime
'global PERMANENTTYPES'
PERMANENTTYPES = [
    'Land', 'Creature', 'Artifact', 'Enchantment', 'Planeswalker', 'Battle'
]

DEBUG = True

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
               controller=None,
               cost = {}):
    self.name = name
    self.basename = name
    self.color = color
    self.text = text
    self.cost = cost
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
    self.object_id = None
    if self.owner is not None and self.object_id is None:
      self.object_id = len(self.owner.game.objects) + 1
      self.owner.game.objects[self.object_id] = self
    if self.controller is not None and self.object_id is None:
      self.object_id = len(self.controller.game.objects) + 1
      self.controller.game.objects[self.object_id] = self
    
    self.hash = self.__hash__()
    return None
  
  def __hash__(self):
    now = datetime.now()
    objectid = 0
    if self.object_id is not None:
      objectid = self.object_id
    self.hash = hash((self.basename,now,objectid,random.random()))
    return self.hash

  #@trace_function
  def __str__(self) -> str:
    return f'{self.name}'


class Card(GameObject):

  #@trace_function
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return None

  #@trace_function
  def can_play_card(self):
    meets_cost = None
    meets_timing = None
    meets_condition = True
    can_play = False
    if self.cost['colorless'] <= self.owner.mana['colorless']:
        meets_cost = True
    if self.controller.game.current_step == 'Main Phase' and (len(self.controller.game.stack.cards)==0):
        meets_timing = True
    if meets_cost and meets_timing and meets_condition:
      can_play = True
    if DEBUG == True:
        ic(self.controller.game.current_step)
        ic(len(self.controller.game.stack.cards))
        ic(meets_cost)
        ic(meets_timing)
        ic(meets_condition)
        ic(can_play)
    return can_play
    



    return False

  #@trace_function
  def cast_spell(self, hand, stack):
    if self.can_play_card():
      hand.remove_card(self)
      self.components["spell"].activate_component()
      stack.add_card(self)
    return self, hand, stack


class Component():

  #@trace_function
  def __init__(self, parent_card: Card):
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
    self.damage = None
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
