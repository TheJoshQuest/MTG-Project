
from icecream import ic
import random
from testing import *

PERMANENTTYPES = ['Land','Creature','Artifact','Enchantment','Planeswalker','Battle']
ZONETYPES = [
            'Library','Hand','Battlefield','Graveyard','Stack','Exile','CommandZone'
            ,'Ante','OutsideTheGame','Sideboard'
            ,'ContraptionDeck','Sprockets','Scrapyard'
            ,'AbsolutelyRemovedFromTheFreakingGameForeverZone'
            ,'AttractionDeck','Junkyard'
            ,'WhammyZone','InterplanarBattlefield'
            ]
    
class Zone():
    @trace_function
    def __init__(self,publiczone: bool = True, sharedzone: bool = True, orderedzone: bool = False):
        self.name = ''
        self.cards = []
        self.publiczone = publiczone
        self.sharedzone = sharedzone
        self.orderedzone = orderedzone
        return None

    @trace_function
    def __str__(self):
        card_names = [card.name for card in self.cards]
        return f"{self.name}: {', '.join(card_names)}"
        
    @trace_function
    def add_card(self, card):
        self.cards.append(card)
        return self.cards

    @trace_function
    def remove_card(self,card):
        self.cards.remove(card)
        return self.cards


class Library(Zone):
    @trace_function
    def __init__(self,deck = None,owner = None,**kwargs):
        super().__init__(publiczone = False, sharedzone = False, orderedzone = True,**kwargs)
        self.name = 'Library'
        self.owner = owner
        if deck is not None:
            self.add_deck(deck,owner)
        return None

    @trace_function
    def add_deck(self,deck,owner):
        for card in deck.cards:
            card.owner = owner
            self.add_card(card)
        return self
        
    @trace_function
    def draw_card(self,player):
        hand = player.hand
        if len(self.cards) > 0:
            card_to_hand = self.cards[0]
            self.remove_card(card_to_hand)
            hand.add_card(card_to_hand)
        return self, hand

    @trace_function
    def shuffle_library(self):
        random.shuffle(self.cards)
        return self
        
class Hand(Zone):
    @trace_function
    def __init__(self,owner = None,**kwargs):
        super().__init__(publiczone = False, sharedzone = False)
        self.name = 'Hand'
        self.owner = owner

    def add_card(self,card):
        card.controller = self.owner
        super().add_card(card)
        return None

class Battlefield(Zone):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Battlefield'
        return None

class Graveyard(Zone):
    @trace_function
    def __init__(self,owner = None,**kwargs):
        super().__init__(sharedzone=False,orderedzone=True,**kwargs)
        self.name = 'Graveyard'
        self.owner = owner
        return None

class Stack(Zone):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(orderedzone=True, **kwargs)
        self.name = 'Stack'
        return None

    @trace_function
    def resolve_stack(self,battlefield):
        self.cards[0].active_component.resolve_spell(self,battlefield)
        return self, battlefield

class Exile(Zone):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Exile'
        return None


class CommandZone(Zone):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Command Zone'
        return None


class AnteZone(Zone):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Ante Zone'
        return None


class OutsideTheGame(Zone):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(publiczone = False,**kwargs)
        self.name = 'Outside the Game'
        return None


class Sideboard(OutsideTheGame):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(publiczone = False,**kwargs)
        self.name = 'Sideboard'
        return None



class ContraptionDeck(Library):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Contraption Deck'
        return None


class Sprockets(Battlefield):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Sprockets'
        return None


class Scrapyard(Graveyard):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Scrapyard'
        return None


class AbsolutelyRemovedFromTheFreakingGameForeverZone(Exile):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Absolutely Removed From The Freaking Game Forever Zone'
        return None


class AttractionDeck(Library):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Attraction Deck'
        return None


class Junkyard(Graveyard):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Junkyard'
        return None


class WhammyZone(Library):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(publiczone = False, sharedzone = False, orderedzone = True,**kwargs)
        self.name = 'Whammy Zone'
        return None


class InterplanarBattlefield(Battlefield):
    @trace_function
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.name = 'Interplanar Battlefield'
        return None