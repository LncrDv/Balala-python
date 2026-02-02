import deckManager, helper
handSize = 9

currentHand = []
#Drawing Hand logic
def DrawHand(_handSize = handSize):
    global handSize
    handSize = _handSize
    global currentHand

    for i in range(_handSize):
        currentHand.append(deckManager.full_deck.pop(0))
