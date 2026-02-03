from handManager import DrawXAdditionnalCards, DiscardCards
from selectionManager import selectedCards
from helper import GetCardsValue
import ui_state

inRound = True

maxHand = 3
maxDiscards = 3
handsLeft = maxHand
discardsLeft = maxDiscards
totalScore = 0

def CalculateChips():
    chipsScore = 0
    for selectedCard in selectedCards:
        chipsScore += selectedCard.chips
    return chipsScore
def CalculateMult():
    multScore = 1
    for selectedCard in selectedCards:
        multScore += selectedCard.mult
    return multScore
def CalculateHandScore():
    handScore = 0
    handScore = CalculateChips() * CalculateMult()
    return handScore

#Play hand logic
def TryToPlayHand():
    global handsLeft, totalScore
    if handsLeft <= 0:
        print("No more hands !")
        return

    num_cards_to_draw = len(selectedCards)  # store BEFORE discarding
    if num_cards_to_draw >= 1:
        print("Playing hand:", [c.name for c in selectedCards])
        totalScore += CalculateHandScore()
        DiscardCards()
        DrawXAdditionnalCards(num_cards_to_draw)
        handsLeft -= 1
        
        print("Total score : ",totalScore)
    else:
        print("Not enough cards are selected !")
        return
    # Clear selection to avoid residual cards
    selectedCards.clear()
def TryToDiscardHand():
    global discardsLeft
    if discardsLeft <= 0:
        print("No more discards !")
        return

    num_cards_to_discard = len(selectedCards)  # store BEFORE discarding
    if num_cards_to_discard >= 1:
        print("Discarding hand:", [c.name for c in selectedCards])
        DiscardCards()
        DrawXAdditionnalCards(num_cards_to_discard)
        discardsLeft -= 1
    else:
        print("Not enough cards are selected !")
        return
    # Clear selection to avoid residual cards
    selectedCards.clear()
   
def RoundLoop():
    if ui_state.pressedPlayHand:
        print("Trying to play hand:", GetCardsValue(selectedCards))
        TryToPlayHand()
    elif ui_state.pressedDiscardHand:
        print("Trying to discard hand:", GetCardsValue(selectedCards))
        TryToDiscardHand()
    