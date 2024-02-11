from zones import *
from gameobjects import *
from game import *
'from player import *'
from icecream import ic
from testing import *
from player import *


test_creature = Card(name = 'Test Creature', printedpower = 1, printedtoughness= 1, text = '', cardtype = ['Creature'])
test_land = Card(name = 'Test Land', text = '', cardtype = ['Land'])
test_sorcery = Card(name = 'Test Sorcery', text = '', cardtype = ['Sorcery'])


Player1 = Player(name = 'Josh')
Deck1 = Deck(name = 'Test Deck', cards= [test_creature,test_land,test_sorcery])
Game = MagicTheGathering()

Player1.add_deck(deck=Deck1)
Player1.select_deck(deck=Deck1)


Player1.library.shuffle_library()
ic(Player1.library.draw_card(Player1))

ic(Player1.hand.cards)


while True:
    for i, item in enumerate(Player1.hand.cards):
        print(f'{i+1}: {item}')
        if i == len(Player1.hand.cards) - 1:
            print(f'{i+2}: {"Next Step"}')
    try:
        index = int(input('Select a card to cast: ')) -1
        if 0 <= index < len(Player1.hand.cards):
            selected_card = Player1.hand.cards[index]
            print(f'Casting {selected_card}')
            selected_card.cast_spell(Player1.hand,Game.stack)
            break
        if index >= len(Player1.hand.cards):
            if index == len(Player1.hand.cards):
                print('Next Step')
                Player1.library.draw_card(Player1)
                continue
            else:
                print('Invalid index')
        else:
            print('Invalid index')
    except ValueError:
        print('Invalid input')

Game.stack.resolve_stack(Game.battlefield)