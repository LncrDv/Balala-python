from handManager import DrawXAdditionnalCards, DiscardCards
import selectionManager
from helper import GetCardsValue
import ui_state
import handTypesManager
import jokerManager
inRound = True

maxHand = 3
maxDiscards = 10
handsLeft = maxHand
discardsLeft = maxDiscards
totalScore = 0

currentHand_handTypePlusChips = 0
currentHand_scoringPlusChips = 0

currentHand_handTypePlusMult = 0
currentHand_scoringPlusMult = 0

currentHand_handTypeTimesMult = 1
currentHand_scoringTimesMult = 1

currentHand_handTypes = None
currentHand_bestHandType = None

def UpdateScore(_plusChips = 0, _plusMult = 0, _timesMult = 0):
    global currentHand_scoringPlusChips, currentHand_scoringPlusMult, currentHand_scoringTimesMult
    currentHand_scoringPlusChips += _plusChips
    currentHand_scoringPlusMult += _plusMult
    currentHand_scoringTimesMult += _timesMult
    pass
def CalculateChips(_handType):
    global currentHand_handTypePlusChips, currentHand_scoringPlusChips

    currentHand_handTypePlusChips = handTypesManager.handTypes[_handType]["default"]["chips"]
    currentHand_scoringPlusChips = 0

    for selectedCard in selectionManager.selectedCards:
        currentHand_scoringPlusChips += selectedCard.chips

    return currentHand_handTypePlusChips, currentHand_scoringPlusChips
def CalculateMult(_handType):
    global currentHand_handTypePlusMult, currentHand_scoringPlusMult
    global currentHand_bestHandType

    currentHand_handTypePlusMult = handTypesManager.handTypes[_handType]["default"]["mult"]
    currentHand_scoringPlusMult = 0
    for selectedCard in selectionManager.selectedCards:
        currentHand_scoringPlusMult += selectedCard.mult

    return currentHand_handTypePlusMult, currentHand_scoringPlusMult
def CalculateHandScore():
    handScore = 0
    handScore = (currentHand_handTypePlusChips+currentHand_scoringPlusChips) * (currentHand_handTypePlusMult+currentHand_scoringPlusMult)
    return handScore

#Play hand logic
def TryToPlayHand():
    global handsLeft, totalScore
    if handsLeft <= 0:
        print("No more hands !")
        return

    num_cards_to_draw = len(selectionManager.selectedCards)  # store BEFORE discarding
    if num_cards_to_draw >= 1:
        #print("Playing hand:", [c.name for c in selectionManager.selectedCards])

        #Determine hand types in hand
        global currentHand_bestHandType, currentHand_handTypes
        currentHand_handTypes = handTypesManager.DetermineHandTypes(selectionManager.selectedCards, selectionManager.CARD_SELECTION_LIMIT)
        #Determine best hand type from hand types
        currentHand_bestHandType = handTypesManager.DetermineBestHandType(currentHand_handTypes)

        #Apply the hand level to score

        #Calculate Joker impacts
        jokerManager.ApplyJokerEffects()
        #Calculate Hand Score
        totalScore += CalculateHandScore()
        DiscardCards()
        DrawXAdditionnalCards(num_cards_to_draw)
        handsLeft -= 1
        
        #print("Total score : ",totalScore)
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
        #print("Discarding hand:", [c.name for c in selectionManager.selectedCards])
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
        #print("Trying to play hand:", GetCardsValue(selectionManager.selectedCards))
        TryToPlayHand()
    elif ui_state.pressedDiscardHand:
        #print("Trying to discard hand:", GetCardsValue(selectionManager.selectedCards))
        TryToDiscardHand()
    