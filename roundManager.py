from handManager import DrawXAdditionnalCards, DiscardCards
import selectionManager
from helper import GetCardsValue
import ui_state
import handTypesManager

inRound = True

maxHand = 3
maxDiscards = 10
handsLeft = maxHand
discardsLeft = maxDiscards
totalScore = 0

def CalculateChips(_handType):
    chipsScore = handTypesManager.handTypes[_handType]["default"]["chips"]
    addedChipScore = 0
    for selectedCard in selectionManager.selectedCards:
        addedChipScore += selectedCard.chips
    return chipsScore, addedChipScore
def CalculateMult(_handType):
    global currentHand_bestHandType
    multScore = handTypesManager.handTypes[_handType]["default"]["mult"]
    addedMultScore = 0
    for selectedCard in selectionManager.selectedCards:
        addedMultScore += selectedCard.mult
    return multScore, addedMultScore
def CalculateHandScore(_handType):
    handScore = 0
    handScore = (CalculateChips(_handType)[0]+CalculateChips(_handType)[1]) * (CalculateMult(_handType)[0]+CalculateMult(_handType)[1])
    return handScore

#Play hand logic
def TryToPlayHand():
    global handsLeft, totalScore
    if handsLeft <= 0:
        print("No more hands !")
        return

    num_cards_to_draw = len(selectionManager.selectedCards)  # store BEFORE discarding
    if num_cards_to_draw >= 1:
        print("Playing hand:", [c.name for c in selectionManager.selectedCards])

        #Determine hand types in hand
        currentHand_handTypes = handTypesManager.DetermineHandTypes(selectionManager.selectedCards, selectionManager.CARD_SELECTION_LIMIT)
        #Determine best hand type from hand types
        currentHand_bestHandType = handTypesManager.DetermineBestHandType(currentHand_handTypes)

        #Apply the hand level to score

        #Calculate Joker impacts

        #Calculate Hand Score
        totalScore += CalculateHandScore(currentHand_bestHandType)
        DiscardCards()
        DrawXAdditionnalCards(num_cards_to_draw)
        handsLeft -= 1
        
        print("Total score : ",totalScore)
    else:
        print("Not enough cards are selected !")
        return
    # Clear selection to avoid residual cards
    selectionManager.selectedCards.clear()
def TryToDiscardHand():
    global discardsLeft
    if discardsLeft <= 0:
        print("No more discards !")
        return

    num_cards_to_discard = len(selectionManager.selectedCards)  # store BEFORE discarding
    if num_cards_to_discard >= 1:
        print("Discarding hand:", [c.name for c in selectionManager.selectedCards])
        DiscardCards()
        DrawXAdditionnalCards(num_cards_to_discard)
        discardsLeft -= 1
    else:
        print("Not enough cards are selected !")
        return
    # Clear selection to avoid residual cards
    selectionManager.selectedCards.clear()
   
def RoundLoop():
    if ui_state.pressedPlayHand:
        print("Trying to play hand:", GetCardsValue(selectionManager.selectedCards))
        TryToPlayHand()
    elif ui_state.pressedDiscardHand:
        print("Trying to discard hand:", GetCardsValue(selectionManager.selectedCards))
        TryToDiscardHand()
    