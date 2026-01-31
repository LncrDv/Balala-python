from cards import Card, ENHANCEMENT_TO_ATLASCOORDS, SEAL_TO_ATLASCOORDS
from random import shuffle, choice, randint
full_deck = []

def create52CardDeck():
    global full_deck
    full_deck = []
    
    suits = ["Hearts","Clubs","Diamonds","Spades"]
    values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]

    for suit in suits:
        for value in values:
            full_deck.append(Card(
                value,
                suit,
                "None",
                choice(list(ENHANCEMENT_TO_ATLASCOORDS.keys())),
                choice(list(SEAL_TO_ATLASCOORDS.keys())),
                "None",
                bool(randint(0,1))
                ))

    full_deck.reverse()