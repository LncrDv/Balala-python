import deckManager
from cards import Card
from selectionManager import selectedCards
import ui
maxHandSize = 7
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
    # Copy so we can safely iterate
    cards_to_discard = selectedCards.copy()

    for card in cards_to_discard:
        print("Removing:", card.name)
        # Remove the card from currentHand
        slot = currentHand.index(card)
        currentHand.pop(slot)
        ui.cardYOffset.pop(slot)

        # Deselect in UI only — do NOT remove from selectedCards here
        ui.DeselectCard(slot)

    # Clear all selections after discarding
    selectedCards.clear()