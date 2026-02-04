import deckManager
from cards import Card
from selectionManager import selectedCards
import ui
import random
maxHandSize = 8
currentHandSize = 0

currentHand : list[Card]
currentHand = []


# Drawing Hand logic
# Drawing Hand logic
# Drawing Hand logic
# Drawing Hand logic
# Define descending poker order
CARD_SORT_ORDER = {
    'Ace': 14,
    'King': 13,
    'Queen': 12,
    'Jack': 11,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

def card_sort_value(card):
    """Return a numeric value for sorting cards descending (Ace high)."""
    # card.value might be int or str
    val = str(card.value)  # convert everything to string to match dictionary keys
    return CARD_SORT_ORDER[val]

# Drawing Hand logic
def DrawXAdditionnalCards(numberOfAdditionnalCards):
    global currentHandSize

    for _ in range(numberOfAdditionnalCards):
        if len(deckManager.currentDeck) > 0:
            idx = random.randint(0, len(deckManager.currentDeck) - 1)
            new_card = deckManager.currentDeck.pop(idx)
            currentHand.append(new_card)
            ui.cardYOffset.append(0)
        else:
            print("Deck is empty!")

    currentHandSize = len(currentHand)

    # Sort descending (Ace first)
    currentHand.sort(key=card_sort_value, reverse=True)


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
        #print("Removing:", currentHand[slot].name)
        ui.DeselectCard(slot)        # reset offset safely
        currentHand.pop(slot)
        ui.cardYOffset.pop(slot)     # keep lengths in sync

    # Clear selection to avoid residual cards
    selectedCards.clear()
