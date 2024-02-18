from gameobjects import *
from game import *
from icecream import ic
from player import *
from testing import *
from zones import *

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
