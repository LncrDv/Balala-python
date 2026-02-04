from cards import Card, ENHANCEMENT_TO_ATLASCOORDS, SEAL_TO_ATLASCOORDS
from random import choice, randint

full_deck = []
deck_chips_value = []
currentDeck = []
cardSuits = ["Hearts","Clubs","Diamonds","Spades"]
cardValues = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
def create52CardDeck():
    global full_deck
    global currentDeck
    global cardSuits, cardValues
    full_deck = []
    
    
    def_plusChips_value = [2,3,4,5,6,7,8,9,10,10,10,10,11]
    def_plusMult_value = [0,0,0,0,0,0,0,0,0,0,0,0,0]

    for suit in cardSuits:
        for value in cardValues:
            full_deck.append(Card(
                value,
                suit,
                "None",
                "None",
                "None",
                "None",
                False,
                def_plusChips_value[cardValues.index(value)],
                def_plusMult_value[cardValues.index(value)]
                ))


    full_deck.reverse()
    currentDeck = full_deck.copy()