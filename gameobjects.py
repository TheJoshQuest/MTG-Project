
from icecream import ic
from testing import *
'global PERMANENTTYPES'
PERMANENTTYPES = ['Land','Creature','Artifact','Enchantment','Planeswalker','Battle']

class GameObject():
    @trace_function
    def __init__(self,name = '',color = [],text = None,cardtype = None, printedpower = None, printedtoughness = None, owner = None, controller = None):
        self.name = name
        self.color = color
        self.text = text
        self.cardtype = cardtype
        self.printedpower = printedpower 
        self.printedtoughness = printedtoughness
        self.active_component = CardComponent(parent_card=self)
        self.owner = owner
        self.controller = controller
        self.components =   {
                            "spell": SpellComponent(parent_card=self),
                            "permanent": PermanentComponent(parent_card=self),
                            "ability": AbilityComponent(parent_card=self),
                            "card": CardComponent(parent_card=self)
                            }
        return None

    @trace_function
    def __str__(self) -> str:
        return f'{self.name}'


class Card(GameObject):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        return None

    @trace_function
    def can_cast_spell(self):
        return True

    @trace_function
    def cast_spell(self,hand,stack):
        if self.can_cast_spell():
            hand.remove_card(self)
            self.components["spell"].activate_component()
            stack.add_card(self)
        return self, hand, stack


class Component():
    @trace_function
    def __init__(self,parent_card):
        self.parent_card = parent_card
        return None
    
    @trace_function
    def activate_component(self):
        self.parent_card.active_component = self
        return self.parent_card.active_component


class CardComponent(Component):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        return None

class SpellComponent(Component):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        return None

    @trace_function
    def resolve_spell(self,stack,battlefield):
        stack.remove_card(self.parent_card)
        if any(cardtype in self.parent_card.cardtype for cardtype in PERMANENTTYPES):
            self.parent_card.components["permanent"].activate_component()
            battlefield.add_card(self.parent_card)
            self.parent_card.active_component.on_enters_battlefield()
        else:
            self.parent_card.components["card"].activate_component()
            self.parent_card.owner.graveyard.add_card(self.parent_card)
        return self.parent_card.active_component

class PermanentComponent(Component):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.originalpower = self.parent_card.printedpower
        self.originaltoughness = self.parent_card.printedtoughness
        self.power = self.originalpower
        self.toughness = self.originaltoughness
        return None

    @trace_function
    def on_enters_battlefield(self):
        self.power += 1
        self.toughness += 1

class AbilityComponent(Component):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        return None
    
    @trace_function
    def activate_ability(self):
        pass

    @trace_function
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