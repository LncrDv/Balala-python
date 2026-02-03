import deckManager
from cards import Card
from selectionManager import selectedCards
import ui
maxHandSize = 15
currentHandSize = 0

currentHand : list[Card]
currentHand = []


#Drawing Hand logic
def DrawXAdditionnalCards(numberOfAdditionnalCards):
    global currentHandSize

    for _ in range(numberOfAdditionnalCards):
        if len(deckManager.currentDeck) > 0:
            new_card = deckManager.currentDeck.pop(0)
            currentHand.append(new_card)
            ui.cardYOffset.append(0)  # <-- exactly once per new card
            currentHandSize = len(currentHand)
        else:
            print("Deck is empty!")  # No visual feedback yet

def DrawFullHand(_handSize = maxHandSize):

    DrawXAdditionnalCards(_handSize - currentHandSize)      #Calcul du n de cartes qui faut pour compléter la main

#Discarding Hand Logic
def DiscardCards():
    import ui
    # Copy list to avoid modifying while iterating
    cards_to_remove = selectedCards.copy()

    # Get indices in descending order
    slots_to_remove = sorted([currentHand.index(c) for c in cards_to_remove], reverse=True)

    for slot in slots_to_remove:
        print("Removing:", currentHand[slot].name)
        ui.DeselectCard(slot)        # reset offset safely
        currentHand.pop(slot)
        ui.cardYOffset.pop(slot)     # keep lengths in sync

    # Clear selection to avoid residual cards
    selectedCards.clear()
