from handManager import currentHand, DrawXAdditionnalCards
from cards import Card
from deckManager import currentDeck
from selectionManager import selectedCards, DeselectCard
from helper import GetCardsValue
import ui
inRound = True

maxHand, maxDiscards = 3,3
handsLeft, discardsLeft = maxHand, maxDiscards

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

def TryToPlayHand():
    global handsLeft
    if handsLeft <= 0:
        return

    num_cards_to_draw = len(selectedCards)  # store BEFORE discarding
    if num_cards_to_draw >= 1:
        print("Playing hand:", [c.name for c in selectedCards])
        DiscardCards()
        DrawXAdditionnalCards(num_cards_to_draw)
        handsLeft -= 1

    # Clear selection to avoid residual cards
    selectedCards.clear()



        
def RoundLoop(spacebarPressed):
    if spacebarPressed:
        print("Trying to play hand : ", GetCardsValue(selectedCards))
        TryToPlayHand()

    