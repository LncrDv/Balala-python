from cards import Card
from random import shuffle
full_deck = []
def create52CardDeck():
    global full_deck
    full_deck = []
    
    suits = ["Hearts","Clubs","Diamonds","Spades"]
    values = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]

    for suit in suits:
        for value in values:
            full_deck.append(Card(value, suit, "None", "None", "None", "None"))

    shuffle(full_deck)
create52CardDeck()
handSize = 7