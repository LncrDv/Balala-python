import deckManager, helper
handSize = 25

currentHand = []
#Drawing Hand logic
def DrawHand(_handSize = handSize):

    global currentHand

    for i in range(_handSize):
        currentHand.append(deckManager.full_deck.pop(0))
