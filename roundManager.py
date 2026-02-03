from handManager import currentHand, DrawXAdditionnalCards
from cards import Card
from deckManager import currentDeck
from selectionManager import selectedCards, DeselectCard
from helper import GetCardsValue
inRound = True

maxHand, maxDiscards = 3,3
handsLeft, discardsLeft = maxHand, maxDiscards

def DiscardCards():
    for i in range(len(selectedCards)):
        print(i)
        card = selectedCards[0]
        print("Removing the ", card.name)
        DeselectCard(card)
        currentHand.pop(0)
        
        
def TryToPlayHand():
    #Check for number of hands
    if handsLeft <= 0:
        return
    else:
        if len(selectedCards) >= 1:        #Hand has enough cards to be played
            #Calculate Hand Score
            DiscardCards()
            DrawXAdditionnalCards(len(selectedCards))                  #Draw new hand

        
def RoundLoop(spacebarPressed):
    if spacebarPressed:
        print("Trying to play hand : ", GetCardsValue(selectedCards))
        TryToPlayHand()

    