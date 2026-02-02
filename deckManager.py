from cards import Card, ENHANCEMENT_TO_ATLASCOORDS, SEAL_TO_ATLASCOORDS
from random import choice, randint

full_deck = []
deck_chips_value = []

def create52CardDeck():
    global full_deck
    full_deck = []
    
    suits = ["Hearts","Clubs","Diamonds","Spades"]
    values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
    def_chips_value = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    def_mult_value = [0,0,0,0,0,0,0,0,0,0,0,0,0]

    for suit in suits:
        for value in values:
            full_deck.append(Card(
                value,
                suit,
                "None",
                choice(list(ENHANCEMENT_TO_ATLASCOORDS.keys())),
                choice(list(SEAL_TO_ATLASCOORDS.keys())),
                "None",
                bool(randint(0,1)),
                def_chips_value[values.index(value)],
                def_mult_value[values.index(value)]
                ))


    full_deck.reverse()
    print(deck_chips_value)