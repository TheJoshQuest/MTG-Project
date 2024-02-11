from __future__ import annotations
from icecream import ic
import random
from testing import *
from zones import *
from game import *

class Player():
    def __init__(self,name, decks: dict = {}) -> None:
        self.name = name
        self.decks = decks
        self.active_player = False
        self.priority = False
        self.starting_player = False
        self.passed_priority = False
        return None
    
    def add_deck(self,deck_name = '',deck = None):
        if deck is not None:
            deck_name = deck.name
        self.decks[deck_name] = deck

    def select_deck(self,deck_name = '', deck = None,owner = None):
        if deck is not None:
            deck_name = deck.name
        if owner == None:
            owner = self
        self.library = Library(deck=self.decks[deck_name],owner = owner)
        self.hand = Hand(owner = owner)
        self.graveyard = Graveyard(owner = owner)


class Deck():
    def __init__(self,name = '',cards = []) -> None:
        self.name = name
        self.cards = cards
        return None
