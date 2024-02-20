from __future__ import annotations
from icecream import ic
import random
from testing import *
from zones import *
from game import *


class Player():

  def __init__(self, name, decks: dict = {}) -> None:
    self.name = name
    self.decks = decks
    self.game = None
    self.is_active_player = False
    self.priority = False
    self.is_starting_player = False
    self.passed_priority = False
    self.mana = {
        'white': 0,
        'blue': 0,
        'black': 0,
        'red': 0,
        'green': 0,
        'colorless': 0
    }
    self.available_actions = []
    return None
  
  def get_available_actions(self):
    available_actions = []
    seen_cards = set()

    for card in self.hand.cards:
      if card.can_play_card() and card.name not in seen_cards:
        available_actions.append(card)
        seen_cards.add(card.name)

    if "Pass Step" not in available_actions:
      available_actions.append("Pass Step")
    if "Concede" not in available_actions:
      available_actions.append("Concede")
    self.available_actions = available_actions
    return self.available_actions

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

  def concede(self):
    exit()


class Deck():

  def __init__(self, name='', cards=[]) -> None:
    self.name = name
    self.cards = cards
    for card in self.cards:
      card.owner = self
    return None
